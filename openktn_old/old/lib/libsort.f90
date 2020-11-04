!!! FROM sort.f90 (https://www.mjr19.org.uk/IT/sorts/sorts.f90)

MODULE MODULE_SORT

CONTAINS

RECURSIVE SUBROUTINE QUICKSORT(array)

    IMPLICIT NONE

    DOUBLE PRECISION, DIMENSION(:), INTENT(INOUT)::array
    DOUBLE PRECISION :: temp,pivot
    INTEGER :: ii, jj, last, left, right

    last=SIZE(array)

    IF (last.lt.50) THEN
        DO ii=2,last
            temp=array(ii)
            DO jj=ii-1,1,-1
                IF (array(jj).le.temp) EXIT
                array(jj+1)=array(jj)
            END DO
            array(jj+1)=temp
        END DO
        RETURN
    END IF

    temp=array(last/2)
    array(last/2)=array(2)
    IF (temp.gt.array(last)) THEN
        array(2)=array(last)
        array(last)=temp
    ELSE
        array(2)=temp
    END IF
    IF (array(1).gt.array(last)) THEN
        temp=array(1)
        array(1)=array(last)
        array(last)=temp
    END IF
    IF (array(1).gt.array(2)) THEN
        temp=array(1)
        array(1)=array(2)
        array(2)=temp
    END IF
    pivot=array(2)

    left=3
    right=last-1
    DO
        DO WHILE(array(left).lt.pivot)
            left=left+1
        END DO
        DO WHILE(array(right).gt.pivot)
          right=right-1
        END DO
        IF (left.ge.right) EXIT
        temp=array(left)
        array(left)=array(right)
        array(right)=temp
        left=left+1
        right=right-1
    END DO
    IF (left.eq.right) left=left+1
    CALL QUICKSORT(array(1:left-1))
    CALL QUICKSORT(array(left:))

END SUBROUTINE QUICKSORT

RECURSIVE SUBROUTINE QUICKSORT_ARG(array, arg)

    IMPLICIT NONE

    DOUBLE PRECISION, DIMENSION(:), INTENT(INOUT)::array
    INTEGER, DIMENSION(:), INTENT(INOUT)::arg
    DOUBLE PRECISION :: temp,pivot
    INTEGER :: temparg
    INTEGER :: ii, jj, last, left, right


    last=SIZE(array)

    IF (last.lt.50) THEN
        DO ii=2,last
            temp=array(ii)
            temparg=arg(ii)
            DO jj=ii-1,1,-1
                IF (array(jj).le.temp) EXIT
                array(jj+1)=array(jj)
                arg(jj+1)=arg(jj)
            END DO
            array(jj+1)=temp
            arg(jj+1)=temparg
        END DO
        RETURN
    END IF

    temp=array(last/2)
    temparg=arg(last/2)
    array(last/2)=array(2)
    arg(last/2)=arg(2)
    IF (temp.gt.array(last)) THEN
        array(2)=array(last)
        arg(2)=arg(last)
        array(last)=temp
        arg(last)=temparg
    ELSE
        array(2)=temp
        arg(2)=temparg
    END IF
    IF (array(1).gt.array(last)) THEN
        temp=array(1)
        temparg=arg(1)
        array(1)=array(last)
        arg(1)=arg(last)
        array(last)=temp
        arg(last)=temparg
    END IF
    IF (array(1).gt.array(2)) THEN
        temp=array(1)
        temparg=arg(1)
        array(1)=array(2)
        arg(1)=arg(2)
        array(2)=temp
        arg(2)=temparg
    END IF
    pivot=array(2)

    left=3
    right=last-1
    DO
        DO WHILE(array(left).lt.pivot)
            left=left+1
        END DO
        DO WHILE(array(right).gt.pivot)
          right=right-1
        END DO
        IF (left.ge.right) EXIT
        temp=array(left)
        temparg=arg(left)
        array(left)=array(right)
        arg(left)=arg(right)
        array(right)=temp
        arg(right)=temparg
        left=left+1
        right=right-1
    END DO
    IF (left.eq.right) left=left+1
    CALL QUICKSORT_ARG(array(1:left-1), arg(1:left-1))
    CALL QUICKSORT_ARG(array(left:), arg(left:))


END SUBROUTINE QUICKSORT_ARG

SUBROUTINE ARGSORT(array, arg)

    DOUBLE PRECISION, DIMENSION(:), INTENT(IN)::array
    DOUBLE PRECISION, DIMENSION(SIZE(array))::aux_array
    INTEGER, DIMENSION(:), INTENT(OUT)::arg
    INTEGER:: n, ii

    aux_array(:)=array(:)

    n=SIZE(array)

    arg = (/ (ii, ii=1, n) /)

    CALL QUICKSORT_ARG(aux_array, arg)

END SUBROUTINE ARGSORT

SUBROUTINE ARGSORT_REVERSE(array,arg)

    IMPLICIT NONE

    DOUBLE PRECISION, DIMENSION(:), INTENT(IN)::array
    DOUBLE PRECISION, DIMENSION(SIZE(array))::aux_array
    INTEGER, DIMENSION(:), INTENT(OUT):: arg
    INTEGER:: n, ii
    INTEGER::head, tail, temp

    aux_array(:)=array(:)

    n=SIZE(array)

    arg = (/ (ii, ii=1,n) /)

    CALL QUICKSORT_ARG(aux_array, arg)

    head = 1
    tail = n
    DO                        
       IF (head >= tail)  EXIT
       temp    = arg(head)
       arg(head) = arg(tail)
       arg(tail) = temp
       head    = head + 1     
       tail    = tail - 1     
    END DO                    

END SUBROUTINE ARGSORT_REVERSE

END MODULE MODULE_SORT
