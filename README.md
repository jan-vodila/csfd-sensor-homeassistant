# CSFD HomeAssistant Sensor

Custom component that adds top 3 movies as new entities from [CSFD](http://www.csfd.sk) website.

## Installation
- Just copy directory `csfd` to your `<config dir>/custom_components` directory.
- Restart Home-Assistant.
- New entities should be available called: `sensor.csfd_movie_1`, `sensor.csfd_movie_2`, `sensor.csfd_movie_3`

## Notes

Currently it is hardcoded that only top 3 movies are fetched from the theatres in Bratislava.

## Next Steps
- Dynamically select the location: One improvement would be to allow the sensor to dynamically select the location, rather than hardcoding it to only fetch movies from theatres in Bratislava. This could be done by allowing the user to specify the location as a configuration option.
- Fetch more than 3 movies: Another improvement would be to allow the sensor to fetch more than just the top 3 movies. This could be done by allowing the user to specify the number of movies to fetch as a configuration option.
- Allow user to choose the number of days in advance: The sensor could also be improved by allowing the user to choose the number of days in advance to show movies, as some users may be interested in seeing movies that will be showing in the future.
- Showing movie trailers: The sensor could be further improved by allowing users to watch movie trailers of the selected movie.

In general, the sensor can be made more flexible and customizable by allowing the user to specify various options for the sensor's behavior, and integrating with other services to fetch more detailed information about the movies.
