import os
import json
import numpy as np
from PIL import Image
from datetime import datetime
from eval import Eval
from env.thor_env import ThorEnv


class EvalTask(Eval):
    '''
    evaluate overall task performance
    '''

    @classmethod
    def run(cls, model, resnet, task_queue, args, lock, successes, failures, results):
        '''
        evaluation loop
        '''
        # start THOR
        env = ThorEnv()

        while True:
            if task_queue.qsize() == 0:
                break

            task = task_queue.get()

            try:
                traj = model.load_task_json(task)
                r_idx = task['repeat_idx']
                print("Evaluating: %s" % (traj['root']))
                print("No. of trajectories left: %d" % (task_queue.qsize()))
                cls.evaluate(env, model, r_idx, resnet, traj, args, lock, successes, failures, results)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("Error: " + repr(e))

        # stop THOR
        env.stop()


    @classmethod
    def evaluate(cls, env, model, r_idx, resnet, traj_data, args, lock, successes, failures, results):
        # reset model
        model.reset()

        # setup scene
        reward_type = 'dense'
        cls.setup_scene(env, traj_data, r_idx, args, reward_type=reward_type)

        # extract language features
        feat = model.featurize([traj_data], load_mask=False)

        # goal instr
        goal_instr = traj_data['turk_annotations']['anns'][r_idx]['task_desc']

        done, success = False, False
        fails = 0
        t = 0
        reward = 0
        while not done:
            # break if max_steps reached
            if t >= args.max_steps:
                break

            # extract visual features
            curr_image = Image.fromarray(np.uint8(env.last_event.frame))
            feat['frames'] = resnet.featurize([curr_image], batch=1).unsqueeze(0)

            # forward model
            m_out = model.step(feat)
            m_pred = model.extract_preds(m_out, [traj_data], feat, clean_special_tokens=False)
            m_pred = list(m_pred.values())[0]

            # check if <<stop>> was predicted
            if m_pred['action_low'] == cls.STOP_TOKEN:
                print("\tpredicted STOP")
                break

            # get action and mask
            action, mask = m_pred['action_low'], m_pred['action_low_mask'][0]
            mask = np.squeeze(mask, axis=0) if model.has_interaction(action) else None

            # print action
            if args.debug:
                print(action)

            # use predicted action and mask (if available) to interact with the env
            t_success, _, _, err = env.va_interact(action, interact_mask=mask, smooth_nav=args.smooth_nav, debug=args.debug)
            if not t_success:
                fails += 1
                if fails >= args.max_fails:
                    print("Interact API failed %d times" % fails + "; latest error '%s'" % err)
                    break

            # next time-step
            t_reward, t_done = env.get_transition_reward()
            reward += t_reward
            t += 1

        # check if goal was satisfied
        goal_satisfied = env.get_goal_satisfied()
        if goal_satisfied:
            print("Goal Reached")
            success = True


        # postconditions
        pcs = env.get_postconditions_met()
        postcondition_success_rate = pcs[0] / float(pcs[1])

        # SPL
        path_len_weight = len(traj_data['plan']['low_actions'])
        s_spl = (1 if goal_satisfied else 0) * min(1., path_len_weight / float(t))
        pc_spl = postcondition_success_rate * min(1., path_len_weight / float(t))

        # path length weighted SPL
        plw_s_spl = s_spl * path_len_weight
        plw_pc_spl = pc_spl * path_len_weight

        # log success/fails
        lock.acquire()
        log_entry = {'trial': traj_data['task_id'],
                     'type': traj_data['task_type'],
                     'repeat_idx': int(r_idx),
                     'goal_instr': goal_instr,
                     'completed_postconditions': int(pcs[0]),
                     'total_postconditions': int(pcs[1]),
                     'postcondition_success': float(postcondition_success_rate),
                     'success_spl': float(s_spl),
                     'path_weighted_success_spl': float(plw_s_spl),
                     'postcondition_spl': float(pc_spl),
                     'path_weighted_postcondition_spl': float(plw_pc_spl),
                     'path_len_weight': int(path_len_weight),
                     'reward': float(reward)}
        if success:
            successes.append(log_entry)
        else:
            failures.append(log_entry)

        # stats
        num_successes, num_failures = len(successes), len(failures)
        num_evals = len(successes) + len(failures)
        total_path_len_weight = sum([entry['path_len_weight'] for entry in successes]) + \
                                sum([entry['path_len_weight'] for entry in failures])
        completed_postconditions = sum([entry['completed_postconditions'] for entry in successes]) + \
                                   sum([entry['completed_postconditions'] for entry in failures])
        total_postconditions = sum([entry['total_postconditions'] for entry in successes]) + \
                               sum([entry['total_postconditions'] for entry in failures])

        # metrics
        sr = float(num_successes) / num_evals
        pc = completed_postconditions / float(total_postconditions)
        plw_sr = (float(sum([entry['path_weighted_success_spl'] for entry in successes]) +
                                    sum([entry['path_weighted_success_spl'] for entry in failures])) /
                                    total_path_len_weight)
        plw_pc = (float(sum([entry['path_weighted_postcondition_spl'] for entry in successes]) +
                                    sum([entry['path_weighted_postcondition_spl'] for entry in failures])) /
                                    total_path_len_weight)


        # save results
        results['success'] = {'num_successes': num_successes,
                              'num_evals': num_evals,
                              'success_rate': sr}
        results['postcondition_success'] = {'completed_postconditions': completed_postconditions,
                                            'total_postconditions': total_postconditions,
                                            'postcondition_success_rate': pc}
        results['path_length_weighted_success_rate'] = plw_sr
        results['path_length_weighted_postcondition_success_rate'] = plw_pc

        print("-------------")
        print("SR: %d/%d = %.3f" % (num_successes, num_evals, sr))
        print("PC: %d/%d = %.3f" % (completed_postconditions, total_postconditions, pc))
        print("PLW S: %.3f" % (plw_sr))
        print("PLW PC: %.3f" % (plw_pc))
        print("-------------")

        lock.release()

    def create_stats(self):
        '''
        storage for success, failure, and results info
        '''
        self.successes, self.failures = self.manager.list(), self.manager.list()
        self.results = self.manager.dict()

    def save_results(self):
        results = {'successes': list(self.successes),
                   'failures': list(self.failures),
                   'results': dict(self.results)}

        save_path = os.path.dirname(self.args.model_path)
        save_path = os.path.join(save_path, 'task_results_' + datetime.now().strftime("%Y%m%d_%H%M%S_%f") + '.json')
        with open(save_path, 'w') as r:
            json.dump(results, r, indent=4, sort_keys=True)