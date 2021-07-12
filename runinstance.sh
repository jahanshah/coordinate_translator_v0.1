aws ec2 run-instances \
  --image-id ami-0747bdcabd34c712a \
  --key-name docker \
  --count 1 \
  --instance-type t2.micro \
  --iam-instance-profile Name=translator
