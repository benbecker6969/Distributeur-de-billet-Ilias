def AccountConnexion():
    name = "BENHARRAT"
    pinCode = "1207"
    connectionAttempt = 0

    while connectionAttempt < 3:
        userName = input("Entrer votre nom d'utilisateur : ")
        writePinCode = input("Entrer votre Code Pin : ")

        if userName == name and writePinCode == pinCode:
            print("Votre authentification est valide ! Bonjour " + name + " !")
            break
        else:
            print("Votre nom d'authentification ou bien votre mot de passe est incorrect.")
            connectionAttempt += 1

    if connectionAttempt == 3:
        print("Compte bloqué ! Trop de tentatives de connexion ont été faites, contacter votre conseiller bancaire.")

AccountConnexion()