import speedtest as st

def Speed_Test():
    print("Iniciando teste de velocidade... Aguarde.")
    test = st.Speedtest(secure=True)

    print("Obtendo melhor servidor...")
    best = test.get_best_server()
    print(f"Servidor: {best['sponsor']} ({best['name']}, {best['country']})")

    print("Testando velocidade de download...")
    down_speed = test.download()
    down_speed = round(down_speed / 10**6, 2)
    print(f"Download speed: {down_speed} Mbps")

    print("Testando velocidade de upload...")
    up_speed = test.upload()
    up_speed = round(up_speed / 10**6, 2)
    print(f"Upload speed: {up_speed} Mbps")

    ping = round(test.results.ping, 2)
    print(f"Ping: {ping} ms")

if __name__ == "__main__":
    Speed_Test()