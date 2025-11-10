This is a BookMyShow-like ticket booking system. The API supports both user-facing and admin operations.

## Users

User Workflow: <br>
-Register/Login -> /user/ <br>
-Select Location -> /user/explore/locations <br>
-View Movies -> /user/explore/movies-{location_name}?language={name}&genre={genre}&format={format} <br>
-Movie Info -> /user/movies/{movie_id} <br>
-Available Shows -> /user/movies/{location_name}/{movie_name}/buytickets/?format={format}&language={language} <br>
-Seat Availability -> /user/seat_layout/availability?show_id={id}&select_seats={no. of seats} <br>
-Lock Seat -> /user/lock <br>
-Book seat->/user/confirm <br>
-Booking Details -> /user/bookings/{user_id} <br>

Admin Workflow: <br>
-Add movie → /admin/movies/ <br>
-Add artist → /admin/artists/ <br>
-Add Location-> /admin/locations/ <br>
-Add Venue-> /admin/venues/ <br>
-Add Screens-> /admin/screens/ <br>
-Add Schedule-> /admin/schedule/ <br>
-Add Show Timings -> /admin/schedule/timings/?schedule_id={id}&days_ahead={no. of days} <br>


## Environment Variables

{ <br>
    "baseURL": add your localhost<br>
}<br>