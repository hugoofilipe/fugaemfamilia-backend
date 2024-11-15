from datetime import datetime
import pandas as pd

class Reservation:
    def __init__(self, id, nome, phone, email, adultos, criancas, animais, data_de_partida, localidade, hora_da_partida, data_de_chegada, hora_da_chegada, localdepartida, localdechegada, destino, tipo_de_viagem, Pernoitar, tem_experiencia, metodo_de_contacto, extras, questions_and_comments, vem_de_onde):
        self.id = id
        # lets remove a space ate the end of "nome" if it has it, like if nome is "João " it will be "João" 
        self.nome = nome.strip() if nome else ""
        # self.contactos = "contactos"
        self.phone = phone if phone else "None"
        self.email = email if email else "None"
        self.localidade = localidade
        self.metodo_de_contacto = metodo_de_contacto
        self.adultos = 0 if adultos == "Nenhum/a" else adultos
        self.criancas = 0 if criancas == "Nenhum/a" else criancas
        self.pessoas = self.pessoas(self.adultos, self.criancas)
        # self.pessoas = pessoas  # This could be a list [Adulto, Adulto, Criança, nan]
        # self.num_pessoas = len([p for p in self.pessoas if p is not ""])
        self.animais = 0 if animais == "Nenhum/a" else animais
        
        # Dates and hours of departure and arrival
        self.data_de_partida = self.fix_date(data_de_partida)
        self.dia_da_partida = self.data_de_partida.strftime('%d') if isinstance(self.data_de_partida, datetime) else None
        self.mes_da_partida = self.get_month(self.data_de_partida)
        # create a day_of_week attribute to get the day of the week of the date, example Timestamp('2024-09-30 00:00:00') will return 'Segunda-feira'
        self.dia_da_semana_da_partida = self.get_week_day(self.data_de_partida)
        self.hora_da_partida_raw = hora_da_partida
        self.hora_da_partida = self.fix_hours(hora_da_partida)
        self.data_de_chegada = self.fix_date(data_de_chegada)
        self.dia_da_chegada = self.data_de_chegada.strftime('%d') if isinstance(self.data_de_chegada, datetime) else None
        self.mes_da_chegada = self.get_month(self.data_de_chegada)
        self.dia_da_semana_da_chegada = self.get_week_day(self.data_de_chegada)
        self.hora_da_chegada_raw = hora_da_chegada
        self.hora_da_chegada = self.fix_hours(hora_da_chegada)
        self.localdepartida = localdepartida
        self.localdechegada = localdechegada
        self.periodo_dias = self.get_period_days()

        self.destino = destino
        self.Pernoitar = Pernoitar
        self.tipo_de_viagem = tipo_de_viagem
        self.tem_experiencia = tem_experiencia
        self.extras = extras  # This could be a dict with keys like 'Cabo de eletricidade', 'Cadeiras de campismo', etc.
        self.questions_and_comments = questions_and_comments
        self.vem_de_onde = vem_de_onde

    # def __str__(self):
    #     pessoas_str = "\n".join([f"Pessoas [{i+1}]: {p}" for i, p in enumerate(self.pessoas) if p is not None])
    #     extras_str = "\n".join([f"[{k}]: {v}" for k, v in self.extras.items()])
    #     return (f"Nome: {self.nome}\nContactos: {self.contactosss}\n"
    #             f"{pessoas_str}\nData de Partida: {self.data_de_partida}\nHora da Partida: {self.hora_da_partida}\n"
    #             f"Data de Chegada: {self.data_de_chegada}\nHora da Chegada: {self.hora_da_chegada}\nDestino: {self.destino}\n"
    #             f"Tem experiência em usar e conduzir uma autocaravana?: {self.tem_experiencia}\nMetodo de contacto preferido?: {self.metodo_de_contacto}\n"
    #             f"{extras_str}\nQuestions and comments: {self.questions_and_comments}")
    
    def fix_date(self, date_str):
        # date_str is a string like '8/18/2024' with the format '%m/%d/%Y'
        if date_str:
            try:
                date = pd.to_datetime(date_str, format='%m/%d/%Y')
                return date
            except ValueError as e:
                print(f"Error parsing date: {date_str} with error: {e}")
                return None
            
    def get_month(self, date):
        # if data is 2024-01-16 so month is 8 and i need to return january as month 1
        if date:
            month = date.month
            if month == 1:
                return "Janeiro"
            elif month == 2:
                return "Fevereiro"
            elif month == 3:
                return "Março"
            elif month == 4:
                return "Abril"
            elif month == 5:
                return "Maio"
            elif month == 6:
                return "Junho"
            elif month == 7:
                return "Julho"
            elif month == 8:
                return "Agosto"
            elif month == 9:
                return "Setembro"
            elif month == 10:
                return "Outubro"
            elif month == 11:
                return "Novembro"
            elif month == 12:
                return "Dezembro"
            else:
                return f"Error 002: Month {month} is not valid"
            
    def fix_hours(self, hours_str):
        # hours_str is a string like '15:30:00 AM', now i want retunr with the format '%H:%M' like '15:30'
        if hours_str:
            try:
                hours = pd.to_datetime(hours_str, format='%H:%M:%S %p')
                # if says PM i need to add 12 hours to the time
                if hours_str[-2:] == 'PM':
                    hours = hours + pd.Timedelta(hours=12)
                hours = hours.strftime('%H:%M') if isinstance(hours, datetime) else None
                return hours
            except ValueError as e:
                print(f"Error parsing hours: {hours_str} with error: {e}")
                return None
    
    def get_period_days(self):
        # this will pick to dates (data_de_partida and data_de_chegada) and return the difference the number of days between like day 2 and day for is a period pf 3 days
        if self.data_de_partida and self.data_de_chegada:
            diff = self.data_de_chegada - self.data_de_partida
            return (self.data_de_chegada - self.data_de_partida).days + 1
        return f"Error 001: Data de Partida: {self.data_de_partida} and Data de Chegada: {self.data_de_chegada} are not valid dates"
    
    def get_week_day(self, date):
        # date is a datetime object like Timestamp('2024-09-30 00:00:00') and i want to return the day of the week like 'Segunda-feira'
        if date:
            days = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
            return days[date.weekday()]
        return "Error 003: Date is not valid"
    
    def pessoas(self, adultos, criancas):
        # Sum the number of adults and children, but adults must be a number and children can be a number, not a string like 'Nenhum/a'
        # if adults is 2 and children is 1, so i will return value 3.
        persons = 0
        if isinstance(adultos, int):
            persons += adultos
        if isinstance(criancas, int):
            persons += criancas
        return persons