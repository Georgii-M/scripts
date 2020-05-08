import json

input_file = input("Please select your JSON file: ")

with open(input_file) as json_file:
    data = json.load(json_file)
    block_string = ''
    for p in data['ResourceRecordSets']:

        val_list = []
        for num in range(len(p['ResourceRecords'])):
            val_list.append(p['ResourceRecords'][num]['Value'])

        # Vars block ---------------
        typeLower = p['Type'].lower()
        typeUpper = p['Type'].upper()
        nameReplacedot = p['Name'].replace('.','_')
        nameWithoutDot = p['Name'][:-1]
        name = p['Name']
        type = p['Type']
        ttl = p['TTL']
        # --------------------------

        block_string += """# terraform import aws_route53_record.%s%s ZBVO6T2U0SW94_%s_%s
        resource "aws_route53_record" "%s%s" {
          count = local.environment == "production" ? 1 : 0

          zone_id = "${aws_route53_zone.suitepad_systems.zone_id}"
          name    = "%s"
          type    = "%s"
          ttl     = "%s"
          records = %s
        }                
        """%(nameReplacedot,typeLower,nameWithoutDot,typeUpper,
             nameReplacedot,typeLower,
             name,type,ttl,val_list)


file = open("converter_output.tf", "w+")

file.write(block_string)

file.close()
