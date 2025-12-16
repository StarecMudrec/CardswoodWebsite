from hashlib import md5

# Параметры из вашего URL
MNT_ID = "74025788"
MNT_TRANSACTION_ID = "f0baf284-c1de-415f-a2bf-3f581e4c291a"
MNT_AMOUNT = "100.00"
MNT_CURRENCY_CODE = "643"
MNT_SUBSCRIBER_ID = ""  # Пустая строка, если не используется
MNT_TEST_MODE = "0"
# ВАЖНО: Замените на реальный MNT_INTEGRITY_CODE из вашего .env файла
MNT_INTEGRITY_CODE = "ВАШ_РЕАЛЬНЫЙ_КОД_ИЗ_ENV"

# Формула согласно документации:
# md5(MNT_ID + MNT_TRANSACTION_ID + MNT_AMOUNT + MNT_CURRENCY_CODE + MNT_SUBSCRIBER_ID + MNT_TEST_MODE + MNT_INTEGRITY_CODE)
raw = MNT_ID + MNT_TRANSACTION_ID + MNT_AMOUNT + MNT_CURRENCY_CODE + MNT_SUBSCRIBER_ID + MNT_TEST_MODE + MNT_INTEGRITY_CODE

print("Строка для подписи:")
print(repr(raw))
print()
print("Вычисленная подпись:")
computed_signature = md5(raw.encode("utf-8")).hexdigest()
print(computed_signature)
print()
print("Подпись из URL:")
url_signature = "271ce0852845bae2d7842a5621129ccf"
print(url_signature)
print()
print("Совпадают?", computed_signature == url_signature)