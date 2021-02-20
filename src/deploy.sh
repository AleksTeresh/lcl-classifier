rsync -a --exclude 'client/node_modules' --exclude 'postgres' ./ ubuntu@195.148.21.214:/home/ubuntu/projects/lcl-classifier/newvolume/src

ssh -l ubuntu 195.148.21.214 "cd /home/ubuntu/projects/lcl-classifier/newvolume/src; docker-compose up --build -d"
