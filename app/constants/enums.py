from enum import Enum

######## Movie Enums #########

class LanguageEnum(str,Enum):
    ENGLISH = "English"
    HINDI = "Hindi" 
    TAMIL = "Tamil"
    KANNADA = "Kannada"
    TELUGU = "Telugu"
    MALAYALAM = "Malayalam"
    MARATHI = "Marathi"
    SANSKRIT = "Sanskrit"

class FormatEnum(str,Enum):
    _2D = "2D"
    _3D = "3D"
    _4DX = "4DX"
    _4DX_3D = "4DX 3D" 
    IMAX_3D = "IMAX 3D"

class GenreEnum(str,Enum):
    DRAMA = "Drama"
    ACTION = "Action"
    THRILLER = "Thriller"
    COMEDY = "Comedy"
    ADVENTURE = "Adventure"
    ROMANTIC = "Romantic"
    FANTASY = "Fantasy"
    SCIFI = "SciFi"
    FAMILY = "Family"
    SPORTS = "Sports"
    ANIMATION = "Animation"
    DOCUMENTARY = "Documentary"
    MUSICAL = "Musical"

######## Artists Enums #########
class OccupationEnum(str, Enum):
    ACTOR = "Actor"
    MUSICIAN = "Musician"
    SINGER = "Singer"
    PRODUCER = "Producer"
    DIRECTOR = "Director"
    CAMERAMAN = "Cameraman"
    MUSIC_DIRECTOR = "Music Director"
    COMPOSER = "Composer"
    BACKGROUND_SCORE = "Background Score"
    SPECIAL_APPEARANCES = "Special Appearances"
    LYRICIST = "Lyricist"
    WRITER = "Writer"
    SCREENPLAY = "Screenplay"
    DIALOGUE_WRITER = "Dialogue Writer"
    VOICE_CAST = "Voice Cast"

######## Venue Enums #########
class FacilitiesEnum(str, Enum):
    PARKING_FACILITY = "Parking Facility"
    TICKET_CANCELLATION = "Ticket Cancellation"
    F_B = "F&B"
    M_TICKET = "M Ticket"
    FOOD_COURT = "Food Court"

######## Booking Enums #########
class BookingEnum(str, Enum):
    BOOKED = "Booked"
    CANCELLED = "Cancelled"

######## User Gender Enums #########
class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"