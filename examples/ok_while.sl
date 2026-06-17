PROGRAM contador ;
VAR
    i , n : INTEGER ;
BEGIN
    READ ( n ) ;
    i := 0 ;
    WHILE i < n DO
        i := i + 1 ;
    WRITE ( i )
END .
