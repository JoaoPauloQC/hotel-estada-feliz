class Guest():
    def __init__(self,id_guest,complete_name,doc,telephone,email,id_system_user=None):
        self.id_guest = id_guest
        self.complete_name = complete_name
        self.doc = doc
        self.telephone = telephone
        self.email = email
        self.id_system_user = id_system_user


guests = [
    Guest(1, "JoaoPauloQC", "12345678901", "11987654321", "joao.silva@email.com", 1),
    Guest(2, "Maria Oliveira", "23456789012", "21996543210", "maria.oliveira@email.com", 2),
    Guest(3, "Carlos Souza", "34567890123", "31997456123", "carlos.souza@email.com", 3),
    Guest(4, "Ana Pereira", "45678901234", "41996234789", "ana.pereira@email.com", 4),
    Guest(5, "Paulo Costa", "56789012345", "51995123678", "paulo.costa@email.com", 5),
    Guest(6, "Fernanda Lima", "67890123456", "61993214567", "fernanda.lima@email.com", 6),
    Guest(7, "Lucas Almeida", "78901234567", "71992345678", "lucas.almeida@email.com", 7),
    Guest(8, "Juliana Ferreira", "89012345678", "81993456789", "juliana.ferreira@email.com", 8),
    Guest(9, "Rafael Martins", "90123456789", "11991234567", "rafael.martins@email.com", 9),
    Guest(10, "Camila Santos", "11223344556", "21998765432", "camila.santos@email.com", 10),
    Guest(11, "Gustavo Rocha", "22334455667", "31997654321", "gustavo.rocha@email.com", 11),
    Guest(12, "Beatriz Nunes", "33445566778", "41998761234", "beatriz.nunes@email.com", 12),
    Guest(13, "André Gomes", "44556677889", "51996547812", "andre.gomes@email.com", 13),
    Guest(14, "Patrícia Carvalho", "55667788990", "61995432109", "patricia.carvalho@email.com", 14),
    Guest(15, "Ricardo Melo", "66778899001", "71992347890", "ricardo.melo@email.com", 15),
    Guest(16, "Larissa Barros", "77889900112", "81994321098", "larissa.barros@email.com", 16),
    Guest(17, "Eduardo Ramos", "88990011223", "11995432100", "eduardo.ramos@email.com", 17),
    Guest(18, "Sabrina Castro", "99001122334", "21997654310", "sabrina.castro@email.com", 18),
    Guest(19, "Felipe Teixeira", "10111213141", "31994327890", "felipe.teixeira@email.com", 19),
    Guest(20, "Isabela Duarte", "12131415161", "41993214509", "isabela.duarte@email.com", 20),
    Guest(21, "Rodrigo Pinto", "13141516171", "51995437891", "rodrigo.pinto@email.com", 21),
    Guest(22, "Tatiane Ribeiro", "14151617181", "61996543218", "tatiane.ribeiro@email.com", 22),
    Guest(23, "Marcelo Azevedo", "15161718191", "71998765430", "marcelo.azevedo@email.com", 23),
    Guest(24, "Bianca Moraes", "16171819202", "81996543219", "bianca.moraes@email.com", 24),
    Guest(25, "Vitor Farias", "17181920212", "11997456321", "vitor.farias@email.com", 25),
    Guest(26, "Danielle Prado", "18192021222", "21995432987", "danielle.prado@email.com", 26),
    Guest(27, "Thiago Tavares", "19202122232", "31999887766", "thiago.tavares@email.com", 27),
    Guest(28, "Aline Cunha", "20212223242", "41997766554", "aline.cunha@email.com", 28),
    Guest(29, "Caio Monteiro", "21222324352", "51996655443", "caio.monteiro@email.com", 29),
    Guest(30, "Natália Pires", "22232425462", "61995544332", "natalia.pires@email.com", 30)
]