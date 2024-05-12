def cumleyi_ayir(cumle, isaret):
    bolunmus_kisimlar = cumle.split(isaret)
    yeni_kisimlar = []
    for i, kisim in enumerate(bolunmus_kisimlar):
        if i != 0:
            yeni_kisimlar.append(isaret + kisim)
        else:
            yeni_kisimlar.append(kisim)
    return yeni_kisimlar

# Örnek kullanım:
cumle = "MAXLEN-PIT+CIRT-PAT"
isaret = "-"
bolunmus_kisimlar = cumleyi_ayir(cumle, isaret)
yeni_kisimlar = []
for kisim in bolunmus_kisimlar:
    if "+" in kisim:
        yeni_kisimlar.extend(cumleyi_ayir(kisim, "+"))
    else:
        yeni_kisimlar.append(kisim)

print("Bölünmüş kısımlar:")
for kisim in yeni_kisimlar:
    print(kisim[1:])