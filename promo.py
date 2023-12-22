import requests
import threading

file_lock = threading.Lock()

def send_post_request(url, headers, data):
    response = requests.post(url, headers=headers, json=data)
    return response

def extract_token(response_text):
    try:
        token = response_text['token'] # Grab Token from response text
        return token
    except KeyError:
        return None # If token isn't provided return None

def save_to_file(token, file_path):
    if token:
        with file_lock:  # Use the lock to synchronize file writing
            with open(file_path, 'a') as f:
                f.write(f'https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n')

def worker(thread_id, url, headers, data, file_path):
    while True:
        response = send_post_request(url, headers, data)
        if response.status_code == 200:
            response_data = response.json()
            token = extract_token(response_data)
            save_to_file(token, file_path)
            print(f'Process-{thread_id}: Token saved successfully: {token}')
        else:
            print(f'Process-{thread_id}: Request failed with status code: {response.status_code}')

def main():
    url = "https://api.discord.gx.games/v1/direct-fulfillment"

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Content-Length': '56',
        'Content-Type': 'application/json',
        'Origin': 'https://www.opera.com',
        'Referer': 'https://www.opera.com/',
        'Sec-Ch-Ua': '"Chromium";v="118", "Opera GX";v="104", "Not=A?Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0 (Edition std-2)'
    }

    data = {
        'partnerUserId': 'fd4b4a4e-49e1-4eac-984c-f3eca489a8fc'
    }

    file_path = 'output/promos.txt'

    num_threads = int(input("Enter the number of threads: "))
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i + 1, url, headers, data, file_path))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
