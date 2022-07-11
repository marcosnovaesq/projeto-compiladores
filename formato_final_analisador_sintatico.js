/*
Testes:
int x;
int x[10];
int x()
void main(void){
    return 1;
}

void main(void){
    if (1>0)
    {
        return 1;
    }
    else 
    {
        return 0;
    }
}
*/


//int x[10];


{
    TIPO: DECLARATION-LIST
    CHILD:[
        {
            TIPO: DECLARATION,
            CHILD: [
                {
                    TIPO: VAR_DECLARATION,
                    CHILD:[
                        {
                            TIPO: TYPE-SPECIFIER,
                            CHILD: [{TIPO: INT, CHILD: []}]
                        },
                        {
                            TIPO: ID, CHILD: []
                        },
                        {
                            TIPO: VAR_DECLARATION_LINHA,
                            CHILD: [
                                {
                                    TIPO: [, CHILD: []
                                },
                                {
                                    TIPO: NUM, CHILD: []
                                },
                                {
                                    TIPO: ], CHILD: []
                                },
                                {
                                    TIPO: ;, CHILD: []
                                },
                            ]
                        },
                    ]
                }
            ]
        }
    ]
}

