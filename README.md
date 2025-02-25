# **libnws**

A Python library for retrieving weather data from the US National Weather Service API. 

> [!WARNING]
> `libnws` is under active development and currently doesn't work. This notice will be removed when it's releasable.
>
> **Timeline**
> - *July 2024* - Project started
> - *September 2024* - Stopped work
> - *February 2025*
>   - Resumed work
>   - Renamed from `nwsc` to `libnws`
>   - Restricted scope to library only

## Contents
- [**libnws**](#libnws)
  - [Contents](#contents)
  - [Features](#features)
  - [Example Usage](#example-usage)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Documentation](#documentation)
  - [Purpose](#purpose)
  - [Acknowledgements](#acknowledgements)
  - [License](#license)
  - [Contributing](#contributing)

## Features
- Retrieves data from all available NWS API endpoints (see [endpoint coverage](docs/endpoint_coverage.md) for details)
- Returns measurements in both metric and imperial
- Supported output formats:
  - CSV
  - JSON
  - Plain-text
  - [Rich-text](https://github.com/Textualize/rich)
- Supported output destinations:
  - SQLite
  - PostgreSQL
  - File (CSV, JSON, or plain text)
  - STDOUT

## Example Usage
To get the weather and the extended forecast in JSON for an address:

```python
import libnws

address = '33 Thomas Street., New York, NY 10007'
weather = libnws.get_weather(address=address, format='json')
forecast = libnws.get_forecast(address=address, forecast='extended', format='json')

print(weather)
print(forecast)
```

```console
(output here)
```

To load the hourly forecast for station "KBOS" into a SQLite database:

```python
import libnws

libnws.get_forecast(
    station='KBOS',
    forecast='hourly',
    save_to='sqlite',
    sqlite_path='/path/to/your/sqlite.db' # Omit this to save to ~/.cache/libnws/libnws.db
)
```

See the [examples](examples/README.md) directory for more.

## Dependencies
- [`requests-cache`](https://github.com/requests-cache/requests-cache) is the only required dependency
- [`rich`](https://github.com/Textualize/rich) is an optional dependency

## Installation

To install without `rich`:

```console
pip install libnws
```

To install with `rich`:

```console
pip install 'libnws[rich]'
```

## Documentation
> [!NOTE]
> These markdown files will eventually migrate into the Sphinx docs

- [docs/library_api.md](docs/library_api.md)
- [docs/endpoint_coverage.md](docs/endpoint_coverage.md)
- [docs/system_design.md](docs/system_design.md)
- [docs/configuration.md](docs/configuration.md)

## Acknowledgements
- Architecture diagram was created with [Lucidchart](https://lucidchart.com/)
- Entity-relationship diagrams were created with [SQLFlow](https://sqlflow.gudusoft.com/#/)
- [Bruno](https://www.usebruno.com) and [Swagger UI](https://swagger.io/tools/swagger-ui/) were very helpful for exploring the API
- The NWS IT/API team have been responsive on their [GitHub page](https://github.com/weather-gov/api) and helpful with troubleshooting endpoint issues
- Parts of the CSV and JSON repositories come from [Red Bird](https://red-bird.readthedocs.io/en/stable/)'s repository pattern examples
- Street address geocoding is done using the US Census Bureau's [geocoding service](https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html)

## License
The National Weather Service Library (`libnws`) is made available under the [MIT License](LICENSE.md)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute to `libnws`
