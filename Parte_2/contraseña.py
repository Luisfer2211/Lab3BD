# guardar_contraseña.py

def guardar_contraseña():
    print("🔐 Introduce la contraseña de PostgreSQL.")
    contraseña = input("Contraseña: ").strip()
    
    with open("contraseña.txt", "w", encoding="utf-8") as f:
        f.write(contraseña)
    
    print("✅ Contraseña guardada en 'contraseña.txt'.")

if __name__ == "__main__":
    guardar_contraseña()
