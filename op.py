from hashlib import md5

MNT_ID = "74025788"
MNT_TRANSACTION_ID = "9498e576-c617-4e55-8d5f-8b98ca06ca09"
MNT_AMOUNT = "1.00"
MNT_CURRENCY_CODE = "643"
MNT_TEST_MODE = "0"   # или уберите, если в формуле его нет
MNT_INTEGRITY_CODE = "12345"

raw = MNT_ID + MNT_TRANSACTION_ID + MNT_AMOUNT + MNT_CURRENCY_CODE + MNT_TEST_MODE + MNT_INTEGRITY_CODE
print(md5(raw.encode("utf-8")).hexdigest())