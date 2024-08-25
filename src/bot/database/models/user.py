#
# (c) 2024, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from database.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    tg_user_id = Column(BigInteger, unique=True)
    language = Column(String(16))
    firstname = Column(String(256), nullable=False)
    lastname = Column(String(256))
    username = Column(String(256))

    utm_id = Column(Integer, ForeignKey('utms.id'))

    utm = relationship(argument='UtmModel', back_populates='users')
    consultations = relationship(argument='ConsultationModel', back_populates='user')
