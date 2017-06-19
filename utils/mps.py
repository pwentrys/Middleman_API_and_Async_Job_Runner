import asyncio
import requests
import base64
import subprocess


# _ip = f'192.168.1.172'
# andromeda_port = 8010
# grus_port = 8020
# _job = f'/toast'
# _begin = f'/begin'
# _finish = f'/finish'
# _toast = f'/toast'
# andromeda = f'http://{_ip}:{andromeda_port}'
# grus = f'http://{_ip}:{grus_port}'
# title = f'Andromeda - Job'
# duration = 3
# requests.get(f'{grus}{_toast}/{title}/Begin - {_id}/{duration}')
# await asyncio.sleep(duration)

# requests.get(f'{andromeda}{_job}{_begin}/{_id}')
# await asyncio.sleep(duration)
# _command_decoded = base64.standard_b64decode(_command).decode('utf-8')
# print(str(subprocess.getoutput(str(_command_decoded))))
# requests.get(f'{andromeda}{_job}{_finish}/{_id}')
# requests.get(f'{grus}{_toast}/{title}/Finish - {_id}/{duration}')
# requests.get(f'{andromeda}/mp{_finish}/{_id}')


async def run_async(_id, _command):
    title = f'Andromeda - Job'
    message = f'Begin - {_id}'
    duration = 3
    address = f'http://192.168.1.172:8020/toast'
    _url = f'{address}/{title}/{message}/{duration}'
    requests.get(_url)
    await asyncio.sleep(5)

    requests.get(f'http://192.168.1.172:8010/job/begin/{_id}')
    _command_decoded = base64.standard_b64decode(_command).decode('utf-8')
    print(str(subprocess.getoutput(str(_command_decoded))))
    requests.get(f'http://192.168.1.172:8010/job/finish/{_id}')
    message = f'Finish - {_id}'
    _url = f'{address}/{title}/{message}/{duration}'
    requests.get(_url)
    requests.get(f'http://192.168.1.172:8010/mp/finish/{_id}')
    # print("Async Print")
    # requests.get(f'http://192.168.1.172:8010/toastthis/Andromeda - Finish/Job - {args}')

    # requests.get(f'http://192.168.1.172:8010/mps/finish/{args}')


def run(_id, _command):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_async(_id, _command))
    loop.close()
