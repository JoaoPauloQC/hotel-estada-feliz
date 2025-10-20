from datetime import date, datetime
class Reserva():

    def __init__(self ,id_reserva,
        id_hospede_principal,
        numero_quarto,
        data_checkin,
        data_checkout,
        status_reserva,
        valor_total):
            self.id_reserva  = id_reserva
            self.id_hospede =  id_hospede_principal
            self.numero_quarto =  numero_quarto
            self.data_checkin =  data_checkin
            self.data_checkout =  data_checkout
            self.status_reserva =  status_reserva
            self.valor_total =  valor_total

reservas = [
    Reserva(1, 1, 201, date(2025, 1, 10), date(2025, 1, 15), "Concluída", 850.00),
    Reserva(2, 1, 105, date(2025, 2, 5), date(2025, 2, 9), "Concluída", 600.00),
    Reserva(3, 103, 110, date(2025, 2, 20), date(2025, 2, 25), "Cancelada", 0.00),
    Reserva(4, 104, 402, date(2025, 3, 3), date(2025, 3, 10), "Concluída", 1200.00),
    Reserva(5, 105, 215, date(2025, 3, 12), date(2025, 3, 15), "Concluída", 450.00),
    Reserva(6, 106, 108, date(2025, 3, 20), date(2025, 3, 24), "Concluída", 720.00),
    Reserva(7, 107, 503, date(2025, 4, 2), date(2025, 4, 8), "Concluída", 990.00),
    Reserva(8, 108, 209, date(2025, 4, 14), date(2025, 4, 17), "Cancelada", 0.00),
    Reserva(9, 109, 318, date(2025, 4, 20), date(2025, 4, 25), "Concluída", 875.00),
    Reserva(10, 110, 407, date(2025, 5, 3), date(2025, 5, 10), "Concluída", 1120.00),
    Reserva(11, 111, 306, date(2025, 5, 12), date(2025, 5, 16), "Concluída", 640.00),
    Reserva(12, 112, 112, date(2025, 5, 22), date(2025, 5, 25), "Concluída", 540.00),
    Reserva(13, 113, 508, date(2025, 6, 1), date(2025, 6, 6), "Concluída", 980.00),
    Reserva(14, 114, 410, date(2025, 6, 10), date(2025, 6, 15), "Concluída", 900.00),
    Reserva(15, 115, 217, date(2025, 6, 20), date(2025, 6, 25), "Cancelada", 0.00),
    Reserva(16, 116, 311, date(2025, 7, 1), date(2025, 7, 5), "Concluída", 640.00),
    Reserva(17, 117, 120, date(2025, 7, 10), date(2025, 7, 13), "Concluída", 480.00),
    Reserva(18, 118, 509, date(2025, 7, 20), date(2025, 7, 25), "Concluída", 890.00),
    Reserva(19, 119, 414, date(2025, 8, 2), date(2025, 8, 7), "Concluída", 760.00),
    Reserva(20, 120, 220, date(2025, 8, 12), date(2025, 8, 16), "Cancelada", 0.00),
    Reserva(21, 121, 311, date(2025, 8, 20), date(2025, 8, 25), "Concluída", 820.00),
    Reserva(22, 122, 506, date(2025, 9, 1), date(2025, 9, 6), "Concluída", 950.00),
    Reserva(23, 123, 312, date(2025, 9, 10), date(2025, 9, 15), "Concluída", 870.00),
    Reserva(24, 124, 117, date(2025, 9, 18), date(2025, 9, 20), "Concluída", 340.00),
    Reserva(25, 125, 405, date(2025, 9, 22), date(2025, 9, 28), "Concluída", 1100.00),
    Reserva(26, 126, 214, date(2025, 10, 2), date(2025, 10, 6), "Concluída", 590.00),
    Reserva(27, 127, 507, date(2025, 10, 10), date(2025, 10, 15), "Concluída", 940.00),
    Reserva(28, 128, 113, date(2025, 10, 18), date(2025, 10, 21), "Concluída", 420.00),
    Reserva(29, 129, 319, date(2025, 10, 25), date(2025, 10, 30), "Ativa", 780.00),
    Reserva(30, 130, 415, date(2025, 11, 1), date(2025, 11, 6), "Ativa", 860.00),
]