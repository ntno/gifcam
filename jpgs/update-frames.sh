#http://gifgifs.com/split/
for f in frames/*.gif; do 
    mv -- "$f" "${f%.gif}.jpg"
done
