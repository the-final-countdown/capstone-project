#!/bin/bash
export API_KEY_MOCKAROO=09de4490
export DATABASE_URL=postgres://mahoqaxfatcnpz:fdd1fa73c849e32efb1af5b65c7e03bc38e15eca6857cff77c143ca33dfd5ff3@ec2-50-17-21-170.compute-1.amazonaws.com:5432/d2qudjadh5h758
flask populate-db
