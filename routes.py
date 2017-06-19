from flask import Flask, redirect
from flask_cors import cross_origin
from datetime import datetime, timedelta
# from urllib3 import open
import requests
import base64
import subprocess
from multiprocessing import Process

from config.strings import Strings as s
from config.templates import Templates
from utils.flask_extensions import add_url_vars
from utils.mps import run as Run_MPs

t = Templates(__file__)


def app_routes(app, appname):
    assert isinstance(app, Flask)
    app.t = t
    app.mps = {}

    # ---------------------------------------------------------------------------- #
    #                                                                              #
    #                           Landing Page                                       #
    #                                                                              #
    # ---------------------------------------------------------------------------- #

    @app.route(s.slash)
    @cross_origin()
    def index():
        return """
            Testy test
        """
    add_url_vars(app, s.index, index)

    @cross_origin()
    def toast():
        app.toaster.toast_args({})
        return """
            Testy test
        """
    add_url_vars(app, 'toast', toast)

    @cross_origin()
    def toast_message(message):
        app.toaster.toast_args({'msg': message})
        return """
            Testy test
        """
    add_url_vars(app, 'toast/<string:message>', toast_message)

    @cross_origin()
    def toast_title_message(title, message):
        app.toaster.toast_args({'title': title, 'msg': message})
        return """
            Testy test
        """
    add_url_vars(app, 'toast/<string:title>/<string:message>', toast_title_message)

    @cross_origin()
    def toast_title_message_duration(title, message, duration):
        app.toaster.toast_args({'title': title, 'msg': message, 'duration': duration})
        return """
            Testy test
        """
    add_url_vars(app, 'toast/<string:title>/<string:message>/<int:duration>', toast_title_message_duration)

    @cross_origin()
    def add_job(command=''):
        app.sql.execute(f'INSERT INTO `andromeda`.`jobs` (`command`) VALUES (\'{command}\');')
        app.sql.commit()
        return f"""
            {command}
        """
    add_url_vars(app, 'job/add/<string:command>', add_job)

    def update_queue_insert(_jobs_str, _app):
        if len(_jobs_str) > 0:
            _insert = f'INSERT INTO andromeda.queue (`job_id`, `status_id`) VALUES {_jobs_str[:-1]};'
            _app.sql.execute(_insert)
            _app.sql.commit()

    @cross_origin()
    def update_queue():
        jobs = app.sql.execute(f'SELECT job_id FROM andromeda.queue WHERE status_id > 0;').fetchall()
        app.sql.commit()
        # jobs_list = []
        jobs_list_string = ''
        for job in jobs:
            # jobs_list.append(job[0])
            jobs_list_string += f'{job[0]},'
        if len(jobs_list_string) == 0:
            # jobs_list = [-1]
            jobs_list_string = '-1,'
        jobs_list_string = jobs_list_string[:-1]
        _jobs = app.sql.execute(f'SELECT id, command FROM andromeda.jobs WHERE id NOT IN ({jobs_list_string});').fetchall()
        counter = 0
        _jobs_str = ''
        for _job in _jobs:
            _jobs_str += f'({_job[0]}, 0),'
            counter += 1
            if counter >= 50:
                counter = 0
                update_queue_insert(_jobs_str, app)
                _jobs_str = ''
        if counter > 0:
            update_queue_insert(_jobs_str, app)
        return redirect('/')
    add_url_vars(app, 'job/update', update_queue)

    @cross_origin()
    def count_jobs(type_id=0):
        count = int(app.sql.execute(f'SELECT count(job_id) FROM andromeda.queue WHERE status_id = {type_id};').fetchall()[0][0])
        # if count == 0:
        #    update_queue()
        return f"""
            {count}
        """
    add_url_vars(app, 'job/count', count_jobs)
    add_url_vars(app, 'job/count/<int:type_id>', count_jobs)

    @cross_origin()
    def get_job():
        res = app.sql.execute(f'SELECT J.id, J.command '
                              f'FROM andromeda.queue Q, andromeda.jobs J '
                              f'WHERE J.id = Q.job_id AND Q.status_id = 0 '
                              f'ORDER BY Q.datetime_create ASC LIMIT 1;'
                              ).fetchall()
        if not(len(res) > 0):
            return f'-1, -1'
        res0 = res[0]
        if len(res0) != 2:
            return f'-1, -1'
        return f"""
            {res0[0]}, {res0[1]}
        """
    add_url_vars(app, 'job/get', get_job)

    @cross_origin()
    def mysql_now():
        now = get_now_from_mysql()
        print(type(now))
        return f''' {now} '''
    add_url_vars(app, 'mysql/now', mysql_now)

    def get_now_from_mysql():
        return app.sql.execute(f'SELECT now();').fetchall()[0][0]

    def update_job_status(idval, status):
        toast_str = 'Begin' if status == 1 else 'Finish'
        col_str = f'datetime_{toast_str.lower()}'

        app.sql.execute(f'UPDATE andromeda.queue SET status_id={status}, {col_str}=now() WHERE job_id={idval};')
        app.sql.commit()
        requests.get(f'http://192.168.1.172:8020/toast/Andromeda Job/{toast_str} {idval}/{status}')

    @cross_origin()
    def begin_job(idval=-1):
        update_job_status(idval, 1)
        return f''' Begin: {idval} '''
    add_url_vars(app, 'job/begin/<int:idval>', begin_job)

    @cross_origin()
    def finish_job(idval=-1):
        update_job_status(idval, 2)
        return f''' Finish: {idval} '''
    add_url_vars(app, 'job/finish/<int:idval>', finish_job)

    @cross_origin()
    def run_queue_redirect():
        return redirect(f'/job/run')
    add_url_vars(app, 'job/run/complete', run_queue_redirect)

    @cross_origin()
    def finish_mps(dt):
        print(f'FINISH MPS DT: {dt}')
        if type(dt) != type(1):
            dt = int(dt)

        print(app.mps[dt])
        p = app.mps[dt]
        if p.is_alive():
            print(f'TERMINATING PROCESS')
            p.terminate()
            print(f'TERMINATED PROCESS - {p.is_alive()}')


        del app.mps[dt]
        return redirect(s.slash)
    add_url_vars(app, 'mps/finish/<int:dt>', finish_mps)

    @cross_origin()
    def run_mps():
        ts = int(datetime.utcnow().timestamp())
        p = Process(
                target=Run_MPs,
                args=[ts]
        )
        p.start()

        app.mps[ts] = p
        return redirect(s.slash)
    add_url_vars(app, 'mps/run/test', run_mps)

    @cross_origin()
    def do_toasty_toast(title, message):
        title = f'{title}'
        message = f'{message}'
        duration = 3
        address = f'http://192.168.1.172:8020/toast'
        _url = f'{address}/{title}/{message}/{duration}'
        print(f'Will Request {_url}')
        requests.get(_url)
        return redirect(s.slash)
    add_url_vars(app, 'toastthis/<string:title>/<string:message>', do_toasty_toast)

    @cross_origin()
    def finish_mp(_id):
        print(f'FINISH PROCID DT: {_id}')
        if type(_id) != type(1):
            dt = int(_id)

        print(app.mps[_id])
        p = app.mps[_id]
        if p.is_alive():
            print(f'TERMINATING PROCESS')
            p.terminate()
            print(f'TERMINATED PROCESS - {p.is_alive()}')


        del app.mps[_id]
        try:
            if int(requests.get(f'http://192.168.1.172:8010/job/count/0').text) > 0:
                # id_command = requests.get(f'http://192.168.1.172:8010/job/get').text
                # id_command_split = id_command.split(',')
                # __id = int(id_command_split[0])
                # _command = id_command_split[1]
                # p = Process(
                #     target=Run_MPs,
                #     args=(__id, _command)
                # )
                # p.start()

                # app.mps[__id] = p
                requests.get(f'http://192.168.1.172:8010/job/run')
        except Exception as error:
            print(error)
        return redirect('/job/run')
    add_url_vars(app, 'mp/finish/<int:_id>', finish_mp)

    @cross_origin()
    def run_queue():
        active_count = int(requests.get(f'http://192.168.1.172:8010/job/count/1').text)
        if active_count == 0:
            queue_size = int(requests.get(f'http://192.168.1.172:8010/job/count/0').text)
            if queue_size > 0:
                try:
                    id_command = requests.get(f'http://192.168.1.172:8010/job/get').text
                    id_command_split = id_command.split(',')
                    _id = int(id_command_split[0])
                    _command = id_command_split[1]
                    # requests.get(f'http://192.168.1.172:8010/job/begin/{_id}')
                    # app.sql.execute(f'UPDATE andromeda.queue SET status_id=1 WHERE job_id={_id};')
                    # app.sql.commit()
                    # app.toaster.toast_args({'title': 'Job', 'msg': f'Begin: {_id}'})
                    # update_job_status(_id, 1)

                    p = Process(
                        target=Run_MPs,
                        args=(_id, _command)
                    )
                    p.start()

                    app.mps[_id] = p
                    # _command_decoded = base64.standard_b64decode(_command).decode('utf-8')
                    # print(str(subprocess.getoutput(_command_decoded)))
                    # requests.get(f'http://192.168.1.172:8010/job/finish/{_id}')
                    # app.sql.execute(f'UPDATE andromeda.queue SET status_id=2 WHERE job_id={_id};')
                    # app.sql.commit()
                    # app.toaster.toast_args({'title': 'Job', 'msg': f'Finish: {_id}'})
                    # requests.get(f'http://192.168.1.172:8010/job/finish/{_id}')
                    # update_job_status(_id, 2)

                    return redirect(f'/job/count')
                except Exception as error:
                    print(error)
                return f''' '''
            else:
                app.toaster.toast_args({'title': 'Jobs', 'msg': f'Queue Empty'})

            return f''' {queue_size} '''

        return f''' Already Active Jobs: {active_count} '''
    add_url_vars(app, 'job/run', run_queue)

    @cross_origin()
    def all_job():
        results = app.sql.execute(f'SELECT job_id FROM andromeda.queue WHERE status_id = 0;').fetchall()
        app.sql.commit()
        jobs = []
        jobs_str = ''
        for result in results:
            jobs.append(result[0])
            jobs_str += f'{result[0]}, '

        if len(jobs_str) > 2:
            jobs_str = jobs_str[:-2]
        return f''' {jobs_str} '''
    add_url_vars(app, 'job/all', all_job)

    def get_job_ids_by_status_id(status_id):
        return [job[0] for job in app.sql.execute(f'SELECT job_id FROM andromeda.queue WHERE status_id={status_id};').fetchall()]

    def get_num_job_ids_by_status_id(status_id):
        return app.sql.execute(f'SELECT count(job_id) FROM andromeda.queue WHERE status_id={status_id};').fetchall()[0][0]

    @cross_origin()
    def active_job():
        jobs = get_job_ids_by_status_id(1)
        jobs_str = ''
        for job in jobs:
            jobs_str += f'{job}, '

        if len(jobs_str) > 2:
            jobs_str = jobs_str[:-2]
        return f''' {jobs_str} '''
    add_url_vars(app, 'job/active', active_job)

    @cross_origin()
    def all_job_cmds():
        results = app.sql.execute(f'SELECT command FROM andromeda.jobs;').fetchall()
        jobs = []
        jobs_str = ''
        for result in results:
            jobs.append(result[0])
            jobs_str += f'{base64.standard_b64decode(result[0]).decode("utf-8")}<br>'

        return f''' {jobs_str} '''
    add_url_vars(app, 'job/allcmd', all_job_cmds)
