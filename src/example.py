from services.authentification.ShibbolethSession import ShibbolethSession
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
    
if __name__ == "__main__":
    test_shibboleth_session()