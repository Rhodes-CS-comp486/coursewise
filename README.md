# **Coursewise: The Wise Way to Choose Courses**

## **Project Description**

Coursewise is a web-based platform that utilizes historical enrollment data to predict future course demand, helping students, departments, and administrators make informed decisions about course selection and offering. The application addresses the common problem of overwhelming course demand and insufficient resources to anticipate that demand accurately.

Our solution empowers:

* **Students** to create class schedules that satisfy degree requirements by providing insights into their likelihood of getting into specific courses  
* **Departments** to predict course demand and make data-driven decisions about course offerings, seat allocation, and professor assignments  
* **Administrators** to set effective guidelines and mitigate issues between student needs and department resources

### **Key Features**

* **Personalized Likelihood Prediction** based on:  
  * Professor demand history  
  * Class year enrollment patterns  
  * Student's declared major  
  * Historical course demand data  
* **Data-Driven Decision Making** tools for faculty and administration  
* **Course Planning Tools** that help students stay on track with degree requirements  
* **Resource Allocation Insights** for departments to optimize course offerings  
* **Bottleneck Identification** for academic program improvements

### **System Diagram**

 ![][image1]

Our application follows the standard Django architecture:

* **Frontend**: User interface and data visualization components  
* **Backend**: API server built with Django, handling business logic and predictions  
* **Database**: SQLite storage for historical enrollment data from multiple sources

### **Screenshots**

## 

## 

## 

## 

## 

## 

## **Project Dependencies**

### **Software Libraries**

* **Python**: General programming language  
* **Django**: Web development framework for backend and frontend connection  
* **SQLite**: Database backend for storing and querying enrollment data

### **Runtime Environment**

* PyCharm

### **Backend Services and Products**

* **Database**:  
  * SQLite   
* **Data Sources**:  
  * CSV files from primary course demand page  
  * Files from Registrar's office with detailed enrollment information  
  * Course catalog data (prerequisites and current offerings)

## **Quick Start Guide**

### **Installation Instructions**

#### **Local Installation**			

Clone the repository:   
	Clone the repository using VCS option on Pycharm/Python IDE or use ‘git clone’ in the terminal  
Ex: git clone [https://github.com/Rhodes-CS-comp486/coursewise.git](https://github.com/Rhodes-CS-comp486/coursewise.git)

Create/activate a virtual environment

Install dependencies:  
Install the following packages through your Python IDE

- Django  
- asgiref  
- pip  
- psycopg  
- setuptools  
- sqlparse  
- typing-extensions  
- wheel

### **Run Instructions**

#### **Local Development Server**

Ensure your virtual environment is activated  
Start the development server  
Access the application at http://localhost:8000  
	\- Run the program and access the link  


[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKoAAACICAYAAAB3EnC/AAALFklEQVR4Xu2da6wdVRXHL7WFtCpiEdFqhRgNJoUCbWJ4xdrYcHtLqbQCWqukBVMRMCb2aqPGR4yNH0qNVq0t5Ep7+WAgSKKJiQIhGqNfWk3UKIXQ1kqL0iYIEpTHh5G1T9bMnP/Ze2bvc2a/bteHX2bOnrX3Wnv2L+cx59y5YwePv1IIQuqMYYMgpIiIKmSBiOrA2Ngq4TXwvIRARHUg1iKlRKxzIKJacMeWabWNtUgpEesciKiWkKy8SLEWKwVizV1EtST2e7RUiDV/EdWS91/+RRH1uIiaBSKqiJoFsRYpJWKdg0ZR6y93IeBP177hD0ahoPOINYQCa0kRm3XXisoDLLtiY/HIT3cE42tbtpa5saYumKnz0sH5fjE5njxXXTDRen4GRKXgV5++NzpNRQ8DC4p5QtP1vHRQjufvujo7mmTtEzUVSRlT0a7wSz2OH4uu5qUjV0kZ07k5JUSdqfPSkbuohO78iKgR6GpeCL9y4MLnhu78WIm6cMH16hjxyAM7yv1LLtxQvHBkb3ny68deOX5v8eiDO/oWh7fEr+7fXu4f2r97IGeXC2qaF/Lck/eU72NvXHNrcfLgVFkjz5f3X3qqunJA+y8fmx4Yz0SX86pfUSBR6YMJLryO21asLC45b6JY/K7eBxlqW3/5SrX/z+9frY69ad5Ecelr22d39+ShmBO7escuWjhRnDm3l2vO6yaKv3y7koyOv2N+7xg/JrAGE7rzYyUqsXbVZrUlGZcs3lAsv2pTuXD/PbqveNtb16ljFHPisaniP4f3lqLSQj7++x8VD91/p3p87E93q+3bz12nxsJcDC8EgpPg2pvAsXWQqPPmXqv2zzh9tRKV56BO+IW9Wn+yZ5ua06L3rS/rdxXVB66i/ntPJQZvZ8+q+m9evlJtz5g9Ufz88+PF49srUYkViyoZ62PQsSXn94t65Xvt6uI+A+uLi40nlamLym20cEf+sEf1W/GBm/uOEbzItOg8GXrMon5v21cH8tThk19HNwmuHdts5lWHRH3+0D0q/n//mDaKuvWzk0rUwwf2lH1dRcUah4HPKY83iqgnd1XCTa7qCcqi1vOQqM/V+u3dPF4eq49/183jZQzmbkN3fqxFjYG2YE1bU3su83JFN4arqCzY/m/2ZKuLQlsS9ZZlK9VLPz1e9M4JJSr3m/pUf78FZ1XXQ7kdH9ugm5uIGoGmWkfFRYhU0Z2fU0ZU+oYIx49FU62jkruoVL/uK9U+Ufm7fTyxMTAWbFhkU3v9OOaIAX2davpA2AU0T9uX/xQxraP2K9TYi8o1YG1cH7Y1tTMpfDvVNK8u4TwoQcrQd/5N52ZAVCL0r4uQ6Qf+OFBTWfCYfjKmdgRzhcTnMymCuXMA59A3H2zograko2Aa29TeJSFyCHpEVAcoR8hnRaGic1H5adzXgpqENLV3ic1LlOAHb6L6WlDTuKb2rvA9L6EZEdUSnpPukpngn05F5UVkaXy8/JuENLV3Ac5LZA1Pp6IyPqUxjW1q75IQOQQ9IqoDIXIIekRUB0LkEPR4E7ULcFweG9ua2rskRA5BjxdRu8AkhWt7l4TIIegRUR0IkUPQk42ofKkL2/HSkU9C5BD0ZCMqt3F7/Vom/47W1K8rfI4tNJOlqHjM1N41vscXzGQlKv1OVSekqb1rfI8vmMlKVG7XfYVpau8SU02Cf7IUFdua2rskRA5BT3aimvDxAxjEtSahO5IQtf4eMwa2klMstglhiC4qy4J/sRkSrgFrQ2xiBD8kISqKEwOqo+mvX7lWbBPCEFXUVCRl2kRsOy74Q0St0SZi23HBH8FE1S2yq6h0c+D9D+1U+0sv/kTxwSs3FpvW36HuUUqPL1t6kzpGN+Gl7Xe/1XxbS0RXI9aLbUIYgolK8IeW+g9JUJY2qM+LR/cVj/1ul9rne5YSs2atKu9v+puffWegbxttIrYdF/zhVVQWU8ewN2T7zKbPFbNnX1OKRaJ+4fYt6m7WBx7eWZy38Ab1+LTT3MfGGnXgHIUweBe1vo8LPYyoxLnnrCvFqt9Xn9toe/qc1QP92sD6hHQIJqqOYUX1RVu9QjxE1Bpt9QrxiCrqsO9TfUD/tqetXiEeUUXlGLoLM4oTGptahXhEF5XjCHpWI2lDwc+itnUK8UhCVIaur+I/P7OB8mCbDb5/aC10R1KiDkuoPEI8RFQhC0RUIQtEVCELRFQhC0RUIQtEVCELRFQhC0RUIQtEVCELRFQhC2aUqPLd/cwle1EpB4PHhJmDiCpkQfaiEqHyCPEQUYUsEFGFLEhCVH6PKX+KIpiILirFkDT4x3ahsalViEdUUem6J8WgNDGQP5dOm6iiukjKsXRfKdpe8J6PDRyrb89+83V9bTa01SvEIytRGXpsEpX5+uTWvngb2uoV4pGVqLS1eUYl3vD6NSOLyn+KjXUL4fEuahsoS0yonrb/0CK/J4iDV1HbSFFUqos/5LG4WDPOQ/BP8qLyjXrfff6N6vFHP3yrenxo/+5i8rYt6tboz/xtqvjzr3+gjvN7U4rZ9uUvFW+Zv1btz5t77cDYiE5ClFUXI/gneVEnPnRL+ezGMhEkKu+/cGSv2vJt0rn95MGpcn/hgusHxkZsJLSJEboneVHPOXut2n5k9afV9tEHd6gtifryseli/lm9y1D0DybqMnP/Sy/aUDz7xI+Lv/72hwNjIzYS2sQI3RNVVMJG1hBQHTYflETUOCQhamxZuQasTYdtnNAt0UUl6p+yY0DXS7EmExSPbYJ/khB1VELKEzKXUCGiOhIyl1AhojoSMpdQIaI6EjKXUCGiOhIyl1AhojoSMpdQIaI6EjKXUCGiOhIyl1AhojoSMpdQIaI6EjKXUCGiOhIyl1AhojoSMleu/P3EqwpsHxYaS0R1JGSuHGFJmSeeHoxxgccRUR0JmSs3UNJRn1nrY4iojoTMlRMo5yiiHn5mcAwR1ZGQuXLgyX8NSjWKpNhfRB2SkLlSB2VCML4N7C+ijkDIXCmDIiGuH6KwPyKiOhIyV6qgRAjGt4H9EYoRUR0JmStFUCIE49vA/gjHiaiOhMyVGigRgvFNtH0Iw/FEVEdC5koFer+JEiHYpwnsqwP7iKiOhMyVArprmgj2aaJtPDqOfYisReU7m4SUJ2Su2KBECL18Y58msD/SdKUga1EJvnkF7eMtIn1wqoiKEiEY3wb2RzAeyV5UEofBYz4IlScmKBGC8W1gfwTjdWQvKt++PJRAofLEAiVCML6JLj+EZS8qEVKekLlCgxIhGN8G9kcwvgkR1ZGQuUKCEiEY34TrNVIbkhK1/n4zFDb3RMUasS1n2l6eTZeLTGB/HdjHhiREZWnwvqUh4NxYkwmX2NRpu6bZdLlIB/ZHXC9n1YkuaixBEVsBbeNSByVCML4N7I9gvCtRRU1FUsZGQpuY1EGJEIxvA/sjGD8MImoNGwltYlIGJUIwvg3sj2D8sIioNWwktIlJFZQIwfg2sD+C8aOQlaifvOF2tT3w8M5SLGJ8efW/qC5e9PFy33V8GwltYlIEJUIw3gYcY9Txmsha1DPfuKZYsnhD8eLRfWos2n/pqd53/7+8b7vz+HXBm8B5pIyPa5oMjkO4Xs6yJWtR7/zGV9T2sqU3FXPmXNMnHG3Xrto8MEYTuUnYBkqEYPwwdD2eiaxE9c1MEhWlRDA+dUTUGjNFVJQSwfgcEFFrzARRUUoE43MhqqhEKrKKpGkTXVSCP02jPCFYdsXG7CVt+2FJ7pISSYhKxPx/qFhLTrT9sGSUH4KkRDKiCu6glMhMkZT4P3Nz/E72GGGcAAAAAElFTkSuQmCC>