from abc import ABC, abstractmethod
from uuid import uuid4
from ..Data import *

class AccountManagementServiceInterface(ABC):
    @abstractmethod
    def createAccount(self, user, passwd, conn):
        raise NotImplementedError()
    @abstractmethod
    def getAccount(self, id, conn):
        raise NotImplementedError()
    @abstractmethod
    def loginAccount(self, user, passwd, conn):
        raise NotImplementedError()
    @abstractmethod
    def recordWin(self, id, conn):
        raise NotImplementedError()
    @abstractmethod
    def recordLoss(self, id, conn):
        raise NotImplementedError()