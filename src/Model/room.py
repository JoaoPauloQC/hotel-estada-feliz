class Room():
    def __init__(self,room_number,id_type,cleaningStatus,location):
        self.room_number = room_number
        self.id_type = id_type
        self.cleaningStatus = cleaningStatus
        self.location = location


rooms = [
    Room("101", 1, "Limpo", "Térreo - Ala Leste"),
    Room("102", 2, "Sujo", "Térreo - Ala Oeste"),
    Room("103", 3, "Limpando", "Térreo - Ala Norte"),
    Room("104", 1, "Limpo", "Térreo - Ala Sul"),
    Room("105", 5, "Sujo", "Térreo - Ala Central"),
    Room("201", 2, "Limpo", "1º Andar - Ala Leste"),
    Room("202", 3, "Limpando", "1º Andar - Ala Oeste"),
    Room("203", 4, "Limpo", "1º Andar - Ala Norte"),
    Room("204", 1, "Sujo", "1º Andar - Ala Sul"),
    Room("205", 5, "Limpo", "1º Andar - Ala Central"),
    Room("301", 3, "Limpo", "2º Andar - Ala Leste"),
    Room("302", 4, "Sujo", "2º Andar - Ala Oeste"),
    Room("303", 2, "Limpando", "2º Andar - Ala Norte"),
    Room("304", 1, "Limpo", "2º Andar - Ala Sul"),
    Room("305", 5, "Limpo", "2º Andar - Ala Central"),
    Room("401", 4, "Sujo", "3º Andar - Ala Leste"),
    Room("402", 3, "Limpando", "3º Andar - Ala Oeste"),
    Room("403", 2, "Limpo", "3º Andar - Ala Norte"),
    Room("404", 1, "Sujo", "3º Andar - Ala Sul"),
    Room("405", 5, "Limpo", "3º Andar - Ala Central"),
    Room("501", 3, "Limpo", "4º Andar - Ala Leste"),
    Room("502", 4, "Sujo", "4º Andar - Ala Oeste"),
    Room("503", 1, "Limpando", "4º Andar - Ala Norte"),
    Room("504", 2, "Limpo", "4º Andar - Ala Sul"),
    Room("505", 5, "Sujo", "4º Andar - Ala Central"),
    Room("601", 2, "Limpo", "5º Andar - Ala Leste"),
    Room("602", 3, "Limpando", "5º Andar - Ala Oeste"),
    Room("603", 4, "Limpo", "5º Andar - Ala Norte"),
    Room("604", 1, "Sujo", "5º Andar - Ala Sul"),
    Room("605", 5, "Limpo", "5º Andar - Ala Central")
]
