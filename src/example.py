from services.auth.ShibbolethSession import ShibbolethSession
from services.moodle.MoodleService import MoodleService
from utils.Utils import write_data_to_file
from utils.config import settings

def test_shibboleth_session():
    moodle_session: ShibbolethSession = ShibbolethSession(
        service_base_url='moodle.uni-jena.de',
        idp_base_url='idp.uni-jena.de',
        username=settings.moodle_username,
        password=settings.moodle_password
    )
    moodle_session.login()
    print(moodle_session.get_session().cookies.get_dict())
    print(moodle_session.validate_session())
    print(moodle_session.get_sess_key())

def test_moodle_service_get_courses():
    moodle_session: ShibbolethSession = ShibbolethSession(
        service_base_url='moodle.uni-jena.de',
        idp_base_url='idp.uni-jena.de',
        username=settings.moodle_username,
        password=settings.moodle_password
    )
    moodle_service: MoodleService = MoodleService(moodle_session)
    data = moodle_service.get_all_courses(5)
    write_data_to_file("tmp/testCourses.json", data)

if __name__ == "__main__":
    #test_shibboleth_session()
    test_moodle_service_get_courses()