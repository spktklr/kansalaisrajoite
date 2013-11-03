# coding=utf-8
import model

def session_user(request, db):
	session = request.environ.get('beaker.session')
	if not session:
		print 'beaker.session not available'
		return None
	
	user_id = session.get('user_id')
	
	if not user_id:
		return None
	
	return db.query(model.Kayttaja).filter_by(id=user_id).first()
