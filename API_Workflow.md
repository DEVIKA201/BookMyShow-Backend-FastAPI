This is a BookMyShow-like ticket booking system. The API supports both user-facing and admin operations.

## Users

User Workflow:
-Register/Login -> /user/
-Select Location -> /user/explore/locations
-View Movies -> /user/explore/movies-{location_name}?language={name}&genre={genre}&format={format}
-Movie Info -> /user/movies/{movie_id}
-Available Shows -> /user/movies/{location_name}/{movie_name}/buytickets/?format={format}&language={language}
-Seat Availability -> /user/seat_layout/availability?show_id={id}&select_seats={no. of seats}
-Lock Seat -> /user/lock
-Book seat->/user/confirm
-Booking Details -> /user/bookings/{user_id}

Admin Workflow:
-Add movie → /admin/movies/
-Add artist → /admin/artists/
-Add Location-> /admin/locations/
-Add Venue-> /admin/venues/
-Add Screens-> /admin/screens/
-Add Schedule-> /admin/schedule/
-Add Show Timings -> /admin/schedule/timings/?schedule_id={id}&days_ahead={no. of days}


## Environment Variables

{
    "baseURL": add your localhost
}