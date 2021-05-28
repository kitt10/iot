import re

regex_patterns_forecast_monday = '^(Předpověď  na pondělí \(00-24\))'
for num_line in range(8, len(whole_forecast)):
    match = re.search(regex_patterns_forecast_monday,
                      whole_forecast[num_line][:30])
    if match:
        forecast = results[num_line].split('\n')[1]
        self.reply('Server chmi.cz předpovídá na pondělí. ' + forecast)
        break
else:
    self.reply('Nebylo možno získat data ze serveru chmi.cz')
    return
