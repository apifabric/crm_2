# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 14, 2024 19:31:05
# Database: sqlite:////tmp/tmp.USanevHqGJ/crm_2/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Campaign(SAFRSBaseX, Base):
    """
    description: Stores information about marketing campaigns.
    """
    __tablename__ = 'campaigns'
    _s_collection_name = 'Campaign'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    budget = Column(Float, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    CampaignLeadList : Mapped[List["CampaignLead"]] = relationship(back_populates="campaign")



class Customer(SAFRSBaseX, Base):
    """
    description: Stores customer information including contact details and balance.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    balance = Column(Float, nullable=False)
    created_at = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")



class Department(SAFRSBaseX, Base):
    """
    description: Represents different departments within the company.
    """
    __tablename__ = 'departments'
    _s_collection_name = 'Department'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    # parent relationships (access parent)

    # child relationships (access children)
    EmployeeDepartmentList : Mapped[List["EmployeeDepartment"]] = relationship(back_populates="department")



class Employee(SAFRSBaseX, Base):
    """
    description: Stores employee details including their position in the company.
    """
    __tablename__ = 'employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    email = Column(String(100))

    # parent relationships (access parent)

    # child relationships (access children)
    EmployeeDepartmentList : Mapped[List["EmployeeDepartment"]] = relationship(back_populates="employee")



class Lead(SAFRSBaseX, Base):
    """
    description: Represents sales leads for potential customers.
    """
    __tablename__ = 'leads'
    _s_collection_name = 'Lead'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    interest_level = Column(Integer, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    CampaignLeadList : Mapped[List["CampaignLead"]] = relationship(back_populates="lead")



class Product(SAFRSBaseX, Base):
    """
    description: Represents products that the company offers.
    """
    __tablename__ = 'products'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductSupplierList : Mapped[List["ProductSupplier"]] = relationship(back_populates="product")
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="product")



class Supplier(SAFRSBaseX, Base):
    """
    description: Contains information about suppliers providing products.
    """
    __tablename__ = 'suppliers'
    _s_collection_name = 'Supplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_name = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductSupplierList : Mapped[List["ProductSupplier"]] = relationship(back_populates="supplier")



class CampaignLead(SAFRSBaseX, Base):
    """
    description: Junction table representing leads captured through various campaigns.
    """
    __tablename__ = 'campaign_leads'
    _s_collection_name = 'CampaignLead'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(ForeignKey('campaigns.id'), nullable=False)
    lead_id = Column(ForeignKey('leads.id'), nullable=False)

    # parent relationships (access parent)
    campaign : Mapped["Campaign"] = relationship(back_populates=("CampaignLeadList"))
    lead : Mapped["Lead"] = relationship(back_populates=("CampaignLeadList"))

    # child relationships (access children)



class EmployeeDepartment(SAFRSBaseX, Base):
    """
    description: Junction table to represent many-to-many relationship between employees and departments.
    """
    __tablename__ = 'employee_departments'
    _s_collection_name = 'EmployeeDepartment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    employee_id = Column(ForeignKey('employees.id'), nullable=False)
    department_id = Column(ForeignKey('departments.id'), nullable=False)

    # parent relationships (access parent)
    department : Mapped["Department"] = relationship(back_populates=("EmployeeDepartmentList"))
    employee : Mapped["Employee"] = relationship(back_populates=("EmployeeDepartmentList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Stores information about customer orders.
    """
    __tablename__ = 'orders'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime)
    status = Column(String(50), nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="order")



class ProductSupplier(SAFRSBaseX, Base):
    """
    description: Junction table linking products to their suppliers.
    """
    __tablename__ = 'product_suppliers'
    _s_collection_name = 'ProductSupplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    supplier_id = Column(ForeignKey('suppliers.id'), nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("ProductSupplierList"))
    supplier : Mapped["Supplier"] = relationship(back_populates=("ProductSupplierList"))

    # child relationships (access children)



class OrderDetail(SAFRSBaseX, Base):
    """
    description: Contains detailed information about each product in an order.
    """
    __tablename__ = 'order_details'
    _s_collection_name = 'OrderDetail'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderDetailList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderDetailList"))

    # child relationships (access children)
