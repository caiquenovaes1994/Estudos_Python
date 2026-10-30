from requests import get

ip = input("Digite o IP: ").strip()
url = f"http://ipapi.co/{ip}/json/"

try:
    data = get(url, timeout = 10).json()
    
    if "error" in data:
        print("IP indisponível ou inválido.")
    else:
        print("IP: {data.get('ip')}")
        print("Cidade: {data.get('city')}")
        print("Estado: {data.get('region')}")
        print("Pais: {data.get('country_name')}")
        print("ISP: {data.get('org')}")
        print("Fuso Horario: {data.get('timezone')}")
        print("Latitude: {data.get('latitude')}")
        print("Longitude: {data.get('longitude')}")
except Exception as e:
    print(f"Erro ao buscar IP: {e}")