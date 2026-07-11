import os
import glob
import requests
from datetime import datetime

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
BACKUP_DIR = os.environ.get('BACKUP_DIR', '/tmp/backups')

def send_file(filepath):
    filename = os.path.basename(filepath)
    size = os.path.getsize(filepath) / (1024 * 1024)
    print(f"Uploading {filename} ({size:.1f} MB)...")
    with open(filepath, 'rb') as f:
        res = requests.post(
            f'https://api.telegram.org/bot{TOKEN}/sendDocument',
            data={
                'chat_id': CHAT_ID,
                'caption': f'🗄 Backup: {filename}\n📅 {datetime.now().strftime("%Y-%m-%d %H:%M")}\n📦 {size:.1f} MB'
            },
            files={'document': (filename, f)}
        )
    if res.ok:
        print(f"✅ {filename} uploaded successfully")
    else:
        print(f"❌ Failed to upload {filename}: {res.text}")

def send_message(text):
    requests.post(
        f'https://api.telegram.org/bot{TOKEN}/sendMessage',
        data={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    )

if __name__ == '__main__':
    files = sorted(glob.glob(f'{BACKUP_DIR}/*.gz'))
    
    if not files:
        send_message('❌ No backup files found!')
        exit(1)
    
    send_message(f'🚀 <b>Gnode Backup Started</b>\n📅 {datetime.now().strftime("%Y-%m-%d %H:%M")}\n📁 {len(files)} files to upload')
    
    for f in files:
        send_file(f)
        os.remove(f)
    
    send_message('✅ <b>All backups uploaded successfully!</b>')
