research_management/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── seed.py                       
│   │
│   ├── core/                       
│   │   ├── __init__.py
│   │   ├── config.py               
│   │   ├── exceptions.py           
│   │   └── security.py             
│   ├── db/                         
│   │   ├── __init__.py
│   │   └── database.py             
│   │
│   ├── dependencies/               
│   │   ├── __init__.py
│   │   └── auth_deps.py            
│   │
│   ├── models/                     
│   │   ├── __init__.py
│   │   ├── user.py                 
│   │   ├── research_project.py     
│   │   └── research_task.py        
│   │
│   ├── schemas/                    
│   │   ├── __init__.py
│   │   ├── auth_schemas.py         
│   │   ├── user_schemas.py         
│   │   ├── project_schemas.py      
│   │   └── task_schemas.py         
│   │
│   ├── services/                   
│   │   ├── __init__.py
│   │   ├── auth_service.py         
│   │   ├── user_service.py         
│   │   ├── project_service.py      
│   │   └── task_service.py         
│   │
│   └── routers/                    
│       ├── __init__.py
│       ├── auth.py               
│       ├── users.py          
│       ├── research_project.py  
│       └── research_task.py     
│                  
├── .env                      
├── .env.example                               
├── requirements.txt             
└── README.md                    


