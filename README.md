# Weather (web API interaction):
Application interact with weather API (provider url - http://openweathermap.org) on Flask framework and Bootstrap.

Servise parse a receiving JSON data and build a charts with JavaScript "Highcharts" library.

The diagram displays a weather in city for requested days and builds a graphs of temperature for morning, day and night periods. Available charts for full period and detail graph for single date.

Application using gunicorn web server. To install all dependencies you can use the console command for Makefile (with already installed pip package manager) :

$make install

For running application you can use the console command for Makefile:

$make start
