# Weather (web API interaction):
Application interact with weather API (provider url - http://openweathermap.org) on Flask framework and Bootstrap.

Servise parse a receiving JSON data and build a charts with JavaScript 'Highcharts' library.

The diagram displays a weather in city for requested days and builds a graphs of temperature for morning, day and night periods. Available charts for full period and detail graph for single date.

Application using gunicorne web server. To install all dependencies and run the application, you can use the console command for Makefile, server will be runned with Gunicorn on 0.0.0.0:8000 :

$make start
