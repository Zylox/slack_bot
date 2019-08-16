cp -a $CODEBUILD_SRC_DIR_artifacts/. ~/aftifacts/

bucket=$(aws cloudformation describe-stacks --stack-name $CODEPIPELINE_STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`CodePipelineBucket`].OutputValue' --output text)

aws cloudformation package \
    --template-file ../bot/bot_core.yaml \
    --s3-bucket $bucket
    --output yaml > bot_core_gen.yaml

aws cloudformation deploy \
    --template-file bot_core_gen.yaml \
    --stack-name $BOT_NAME
    --capabilities CAPABILITY_IAM