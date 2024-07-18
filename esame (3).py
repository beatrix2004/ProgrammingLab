class ExamException(Exception):
    pass

class CSVTimeSeriesFile():
    def __init__(self,name):
        self.name=name

    def get_data(self):
        try: 
            with open(self.name, "r") as file:
                data=[]
                past_epoch=None

                for line in file: #controllo per ogni riga e separare valori
                    row=line.strip().split(',')

                    try:
                        epoch=int(float(row[0]))
                        temperature=float(row[1])
                    except ValueError: #se non posso convertire 
                        continue
                    except IndexError:#o mancano valori
                        continue

                    if past_epoch is not None and (past_epoch>epoch or past_epoch==epoch): #controllo duplicati o elementi in "disordine"
                        if past_epoch>epoch:
                            raise ExamException('Errore, timestamp fuori ordine')
                        elif past_epoch==epoch:
                            raise ExamException('Errore, timestamp duplicato')

                    data.append([epoch, temperature])
                    past_epoch=epoch

            return data


        except FileNotFoundError: #se il file non c'è o ci sono errori
            raise ExamException('Errore, file non trovato')
        except:
            raise ExamException('Errore nella lettura del file')



def compute_daily_max_difference(time_series):
    # valuto se la lista è vuota
    if not time_series:
        raise ExamException("Errore, la time_series è vuota.")

    daily_differences = []
    current_day = None
    current_day_temperatures = []

    for entry in time_series: 
        epoch, temperature = entry 
        day_start_epoch = epoch-(epoch%86400)

        if current_day is None:
            current_day = day_start_epoch

        if day_start_epoch != current_day:

            # Calcola la differenza per il giorno precedente
            if len(current_day_temperatures) == 1: #se ho solo una misurazione
                daily_differences.append(None)

            else:
                max_temperature = current_day_temperatures[0]
                min_temperature = current_day_temperatures[0]
                for temp in current_day_temperatures[1:]:
                    if temp > max_temperature:
                        max_temperature = temp
                    if temp < min_temperature:
                        min_temperature = temp

                daily_differences.append(max_temperature-min_temperature)


            # Reset per il nuovo giorno
            current_day = day_start_epoch
            current_day_temperatures = []

        current_day_temperatures.append(temperature) 
    #Aggiungi la temperatura corrente alla lista

    if len(current_day_temperatures) == 1:# Calcola la differenza per l'ultimo giorno 
        daily_differences.append(None)
    else:
        max_temperature = current_day_temperatures[0]
        min_temperature = current_day_temperatures[0]
        for temp in current_day_temperatures[1:]:
            if temp > max_temperature:
                max_temperature = temp
            if temp < min_temperature:
                min_temperature = temp
        daily_differences.append(max_temperature - min_temperature) 

    return daily_differences


if __name__ == "__main__":
    try:
        time_series_file = CSVTimeSeriesFile(name='datatest.csv')
        time_series = time_series_file.get_data()
        differences = compute_daily_max_difference(time_series)

        print(differences)

    except ExamException as e:
        print(f"An error occurred: {e}")
