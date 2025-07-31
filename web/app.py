from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView
from dp.model import engine, User, City, Chat, Message
from web.provider import UsernameAndPasswordProvider

app = Starlette()
admin = Admin(engine,
              title='P_29Admin',
              base_url='/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="sdgfhjhhsfdghn")]
              )
admin.add_view(ModelView(User))
admin.add_view(ModelView(City))
admin.add_view(ModelView(Chat))
admin.add_view(ModelView(Message))

admin.mount_to(app)
