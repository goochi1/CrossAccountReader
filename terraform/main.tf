data "aws_iam_policy_document" "assume_role_policy2" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["${var.identifier}"]
    }
  }
}

data "aws_iam_policy_document" "read_only_policy" {
    statement {
        actions = [
                "acm:Describe*",
                "acm:Get*",
                "acm:List*",
                "apigateway:GET",
                "application-autoscaling:Describe*",
                "appstream:Describe*",
                "appstream:Get*",
                "appstream:List*",
                "athena:List*",
                "athena:Batch*",
                "athena:Get*",
                "autoscaling:Describe*",
                "batch:List*",
                "batch:Describe*",
                "clouddirectory:List*",
                "clouddirectory:BatchRead",
                "clouddirectory:Get*",
                "clouddirectory:LookupPolicy",
                "cloudformation:Describe*",
                "cloudformation:Get*",
                "cloudformation:List*",
                "cloudfront:Get*",
                "cloudfront:List*",
                "cloudhsm:List*",
                "cloudhsm:Describe*",
                "cloudhsm:Get*",
                "cloudsearch:Describe*",
                "cloudsearch:List*",
                "cloudtrail:Describe*",
                "cloudtrail:Get*",
                "cloudtrail:List*",
                "cloudtrail:LookupEvents",
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*",
                "codebuild:BatchGet*",
                "codebuild:List*",
                "codecommit:BatchGet*",
                "codecommit:Get*",
                "codecommit:GitPull",
                "codecommit:List*",
                "codedeploy:BatchGet*",
                "codedeploy:Get*",
                "codedeploy:List*",
                "codepipeline:List*",
                "codepipeline:Get*",
                "codestar:List*",
                "codestar:Describe*",
                "codestar:Get*",
                "codestar:Verify*",
                "cognito-identity:List*",
                "cognito-identity:Describe*",
                "cognito-identity:LookupDeveloperIdentity",
                "cognito-sync:List*",
                "cognito-sync:Describe*",
                "cognito-sync:Get*",
                "cognito-sync:QueryRecords",
                "cognito-idp:AdminList*",
                "cognito-idp:List*",
                "cognito-idp:Describe*",
                "cognito-idp:Get*",
                "config:Deliver*",
                "config:Describe*",
                "config:Get*",
                "config:List*",
                "connect:List*",
                "connect:Describe*",
                "datapipeline:Describe*",
                "datapipeline:EvaluateExpression",
                "datapipeline:Get*",
                "datapipeline:List*",
                "datapipeline:QueryObjects",
                "datapipeline:ValidatePipelineDefinition",
                "directconnect:Describe*",
                "devicefarm:List*",
                "devicefarm:Get*",
                "discovery:Describe*",
                "discovery:List*",
                "discovery:Get*",
                "dms:Describe*",
                "dms:List*",
                "ds:Check*",
                "ds:Describe*",
                "ds:Get*",
                "ds:List*",
                "ds:Verify*",
                "dynamodb:BatchGet*",
                "dynamodb:Describe*",
                "dynamodb:Get*",
                "dynamodb:List*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "ec2:Describe*",
                "ec2:Get*",
                "ecr:BatchCheck*",
                "ecr:BatchGet*",
                "ecr:Describe*",
                "ecr:Get*",
                "ecr:List*",
                "ecs:Describe*",
                "ecs:List*",
                "elasticache:Describe*",
                "elasticache:List*",
                "elasticbeanstalk:Check*",
                "elasticbeanstalk:Describe*",
                "elasticbeanstalk:List*",
                "elasticbeanstalk:RequestEnvironmentInfo",
                "elasticbeanstalk:RetrieveEnvironmentInfo",
                "elasticfilesystem:Describe*",
                "elasticloadbalancing:Describe*",
                "elasticmapreduce:Describe*",
                "elasticmapreduce:List*",
                "elastictranscoder:List*",
                "elastictranscoder:Read*",
                "es:Describe*",
                "es:List*",
                "es:ESHttpGet",
                "es:ESHttpHead",
                "events:Describe*",
                "events:List*",
                "events:TestEventPattern",
                "firehose:Describe*",
                "firehose:List*",
                "gamelift:List*",
                "gamelift:Get*",
                "gamelift:Describe*",
                "gamelift:RequestUploadCredentials",
                "gamelift:ResolveAlias",
                "gamelift:SearchGameSessions",
                "glacier:List*",
                "glacier:Describe*",
                "glacier:Get*",
                "health:Describe*",
                "health:Get*",
                "health:List*",
                "iam:Generate*",
                "iam:*",
                "iam:Simulate*",
                "inspector:Describe*",
                "inspector:Get*",
                "inspector:List*",
                "inspector:LocalizeText",
                "inspector:Preview*",
                "iot:Describe*",
                "iot:Get*",
                "iot:List*",
                "kinesisanalytics:Describe*",
                "kinesisanalytics:DiscoverInputSchema",
                "kinesisanalytics:Get*",
                "kinesisanalytics:List*",
                "kinesis:Describe*",
                "kinesis:Get*",
                "kinesis:List*",
                "kms:Describe*",
                "kms:Get*",
                "kms:List*",
                "lambda:List*",
                "lambda:Get*",
                "lex:Get*",
                "lightsail:Get*",
                "lightsail:Is*",
                "lightsail:Download*",
                "logs:Describe*",
                "logs:Get*",
                "logs:FilterLogEvents",
                "logs:TestMetricFilter",
                "machinelearning:Describe*",
                "machinelearning:Get*",
                "mobilehub:Get*",
                "mobilehub:List*",
                "mobilehub:ValidateProject",
                "mobilehub:VerifyServiceRole",
                "opsworks:Describe*",
                "opsworks:Get*",
                "opsworks-cm:Describe*",
                "organizations:Describe*",
                "organizations:List*",
                "polly:Describe*",
                "polly:Get*",
                "polly:List*",
                "polly:SynthesizeSpeech",
                "rekognition:CompareFaces",
                "rekognition:Detect*",
                "rekognition:List*",
                "rekognition:SearchFaces",
                "rekognition:SearchFacesByImage",
                "rds:Describe*",
                "rds:List*",
                "rds:Download*",
                "redshift:Describe*",
                "redshift:View*",
                "route53:Get*",
                "route53:List*",
                "route53domains:CheckDomainAvailability",
                "route53domains:Get*",
                "route53domains:List*",
                "s3:Get*",
                "s3:List*",
                "s3:Head*",
                "sdb:Get*",
                "sdb:List*",
                "sdb:Select*",
                "servicecatalog:List*",
                "servicecatalog:ScanProvisionedProducts",
                "servicecatalog:Search*",
                "servicecatalog:Describe*",
                "ses:Get*",
                "ses:List*",
                "shield:Describe*",
                "shield:List*",
                "sns:Get*",
                "sns:List*",
                "sqs:Get*",
                "sqs:List*",
                "sqs:ReceiveMessage",
                "ssm:Describe*",
                "ssm:Get*",
                "ssm:List*",
                "states:List*",
                "states:Describe*",
                "states:GetExecutionHistory",
                "storagegateway:Describe*",
                "storagegateway:List*",
                "sts:AssumeRole",
                "support:*",
                "swf:Count*",
                "swf:Describe*",
                "swf:Get*",
                "swf:List*",
                "tag:Get*",
                "trustedadvisor:Describe*",
                "waf:Get*",
                "waf:List*",
                "waf-regional:List*",
                "waf-regional:Get*",
                "workdocs:Describe*",
                "workdocs:Get*",
                "workdocs:CheckAlias",
                "workmail:Describe*",
                "workmail:Get*",
                "workmail:List*",
                "workmail:Search*",
                "workspaces:Describe*",
                "xray:BatchGetTraces",
                "xray:Get*"
        ]

        resources = [
            "*",
        ]
    }
}

resource "aws_iam_policy" "read_only_policy" {
  name   = "ReadOnly"
  path   = "/"
  policy = "${data.aws_iam_policy_document.read_only_policy.json}"
}

resource "aws_iam_role" "cross_iam_role" {
  name               = "CrossAccountReader"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role_policy2.json}"
}

resource "aws_iam_policy_attachment" "read_only_policy_attachment" {
  name       = "policy-attachment"
  policy_arn = "${aws_iam_policy.read_only_policy.arn}"
  roles      = ["${aws_iam_role.cross_iam_role.name}"]
}
