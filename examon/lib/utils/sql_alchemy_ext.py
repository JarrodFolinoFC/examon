class SqlAlchemyExtension:
    @staticmethod
    def get_or_create(session, model, defaults=None, **kwargs):
        instance = session.query(model).filter_by(**kwargs).one_or_none()
        if instance:
            return instance, False
        else:
            kwargs |= defaults or {}
            instance = model(**kwargs)
            try:
                session.add(instance)
                session.commit()
            except Exception:
                session.rollback()
                instance = session.query(model).filter_by(**kwargs).one()
                return instance, False
            else:
                return instance, True
