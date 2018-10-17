%MATLAB code to find triplet embedding and number of triplets which are implied

function X = main(lambd)

    rng(0)
    triplet=load('output/triplet_response.txt');

    %triplet responses starting from 1 to n
    triplet1=1+triplet;

    numsketches=max(triplet1(:))

    %Method used to find embedding
    [X,nc]=gnmds_x(triplet1,2,lambd);
    dlmwrite('output/er.txt',nc,'delimiter','\t');

    %Write coordinates to file
    dlmwrite('output/xx.txt',X,'delimiter','\t');

    [wrongmatr,vec]=impliedt(triplet1,numsketches);

    %print frequency of sketches which are most common among contradicted triplets
    disp('Sketches frequency in contradicted triplets: Higher shows sketch is tough to judge');
    disp(vec);
    end

function [wrongmatr,vec]=impliedt(triplet1,numsketches)
%function returns contradicted triplets and a vector with frequency of
%sketches in contradictions

trip2=(sort(triplet1'))';

[~, idx]=sortrows(trip2);

%wrongsc is count of triplets which are contradictory
wrongsc=0;
rightsc=0;

rightmatr=[];
wrongmatr=[];


for i=1:3:length(triplet1)
    f1=triplet1(idx(i),:); %ABC
    f2=triplet1(idx(i+1),:);
    f3=triplet1(idx(i+2),:);

    %Responses are ABC, BCA, *
    if((f2(1)==f1(2)) && (f2(2)==f1(3)))

        if(f3(2)==f1(1))
            %Third response is CAB
            wrongsc=wrongsc+1;
            wrongmatr=[wrongmatr;[idx(i), idx(i+1), idx(i+2)]];
            %disp('*1ABC, BCA, CAB, Wrong Implied');
            
        else
            %CBA is implied
            rightsc=rightsc+1;
            rightmatr=[rightmatr;i];
            %disp('1ABC, BCA, CBA, Right');
        end
    

    %Responses are ABC, *, BCA
    elseif ((f3(1)==f1(2)) && (f3(2)==f1(3))) 
        
        if(f2(2)==f1(1))
            %Second response is CAB
            wrongsc=wrongsc+1;
            wrongmatr=[wrongmatr;[idx(i), idx(i+1), idx(i+2)]];
            %disp('*1ABC, CAB, BCA Wrong Implied');
        else
            rightsc=rightsc+1;%CBA
            rightmatr=[rightmatr;i];
            %disp('1ABC, CBA, BCA, Right');
        end

    
    %Responses are %ABC, CAB, *      
    elseif ((f2(1)==f1(3)) && (f2(2)==f1(1))) 
        
        if(f3(2)==f1(1))
            %Third response is BAC
            rightsc=rightsc+1;
            rightmatr=[rightmatr;i];
            %disp('2ABC, CAB, BAC Right');
        else
            %Third response is BCA
            wrongsc=wrongsc+1;
            wrongmatr=[wrongmatr;[idx(i), idx(i+1), idx(i+2)]];
            %disp('2ABC, CAB, BCA Wrong Implied');
        end

    %Responses are %ABC, *, CAB     
    elseif ((f3(1)==f1(3)) && (f3(2)==f1(1))) %ABC, *, CAB
        
        if(f2(2)==f1(1))
            rightsc=rightsc+1;
            rightmatr=[rightmatr;i];
            %disp('2ABC, BAC, CAB Right');
        else
            wrongsc=wrongsc+1;%BCA
            wrongmatr=[wrongmatr;[idx(i), idx(i+1), idx(i+2)]];
            %disp('2ABC, BCA, CAB Wrong Implied');
            
        end
        
    else
        rightmatr=[rightmatr;i];
    end
    
end

% Write number of implied triplets
swrng=size(wrongmatr);
dlmwrite('output/wrongmatr.txt',wrongmatr,'delimiter','\t');

disp('Number of transitive violations')
disp(swrng);

%Find frequency of each sketch in the contradicted triplets
vec=zeros(10,1);
for i=1:swrng(1)
    for j=1:3
       vec(triplet1(wrongmatr(i,j)))=vec(triplet1(wrongmatr(i,j)))+1;
    end
end



end




