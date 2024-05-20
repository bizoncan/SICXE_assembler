with open("hata.txt", 'w') as dosya:
    dosya.seek(0)  # Dosyanın başına git
    dosya.truncate()
    for hatacik in hatalar:
        dosya.write(hatacik)