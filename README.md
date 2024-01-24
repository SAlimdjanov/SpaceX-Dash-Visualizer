# SpaceX Launch Data Dash Visualizer

A clean and simple dashboard application that visualizes outcomes of SpaceX Falcon 9 Launches. The [dataset](https://www.kaggle.com/datasets/scoleman/spacex-launch-data/data) was downloaded from Kaggle.

## Functionality

One can filter plot outputs by:

-   Selecting a launch site using the dropdown menu
-   Utilizing the slider to select launches within a certain range of payload masses

### Libraries

-   **dash**: Creation of HTML dash application and plots
-   **pandas**: Loading .csv data into a DataFrame, for plotting by plotly dash
-   **numpy**: Numerical manipulation of data

## Tools Used

-   Docker
-   AWS (EC2)

## Starting the Application (Locally)

Build and start the application container by running:

`docker-compose up --build`

The application will be available at http://localhost:9000.

## Deployment to AWS

After creating an EC2 instance on Amazon Linux 2 and a key pair, open the instance console. Run the following commands:

Update the yum package manager:

`sudo update yum -y`

Install Docker on the virtual machine:

`sudo amazon-linux-extras install docker`

Run Docker:

`sudo service docker start`

With Docker now running, grant all permissions to the VM user (default name is ec2-user):

`sudo usermod -a -G docker ec2-user`

Create a folder and step into it. Print the working directory and save it for a later step. Back in your IDE, place the `.pem` file in the root directory of the project. Then, modify its permissions to be read-only:

`chmod 600 file-name.pem`

Don't forget to do this. An error will occur on the EC2 instance when you attempt to upload it without the permissions being modified.

In a terminal on your local machine, upload the project files to your EC2 instance on the cloud, using the instance's **public** IP address and the directory you created on the VM:

`scp -i file-name.pem Dockerfile {APP_FILES} requirements.txt ec2-user@{PUBLIC_IP}:{DIRECTORY_YOU_CREATED}`

Type `yes` when prompted to continue with the connection.

Go back to the EC2 instance in the browser. Run the command below to build the Docker container with the Dockerfile:

`docker build -t ec2-spacex-dash:v1.0 -f Dockerfile .`

Sometimes a permission denied error will occur. If so, run the same command with the `sudo` prefix.

Now, run the command to see the Docker images:

`sudo docker images`

Run the image as a container, in detach mode `-d` specifying ports `-p` where 80 is the HTTP request entry point and 9000 is the port specified in the dash application:

`sudo docker run -d -p 80:9000 ec2-dash:v1.0`

Run the following to see the run status:

`sudo docker ps`

Type the public IP address specified in the EC2 instance in a browser and the application should be live and publicly visible:

![aws-deploy](/assets/aws-deploy-screenshot.png)

## Cleanup

To stop the container, run:

`sudo docker stop {CONTAINER_ID}`

Then, navigate to the EC2 main page on AWS and select the instance. Click "Terminate" to shut down the virtual machine.
