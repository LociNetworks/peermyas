from flask import Flask, render_template, request, flash
import requests

app = Flask(__name__)
app.secret_key = #'REPLACE WITH SECRET KEY'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':

        # Get Your AS Information
        asn1 = request.form['asn1']
        asn1_u = 'https://www.peeringdb.com/api/net?asn=%s&depth=2' % asn1
        try:
            asn1_r = requests.get(asn1_u)
            asn1_r.raise_for_status()
        except requests.exceptions.HTTPError:
            flash('Your AS Number is not valid or not in PeeringDB. Please verify and try again')
            return render_template('index.html')
        asn1_d = asn1_r.json()

        # Get Peer AS Information
        asn2 = request.form['asn2']
        asn2_u = 'https://www.peeringdb.com/api/net?asn=%s&depth=2' % asn2
        try:
            asn2_r = requests.get(asn2_u)
            asn2_r.raise_for_status()
        except requests.exceptions.HTTPError:
            flash('Peer AS Number is not valid or not in PeeringDB. Please verify and try again')
            return render_template('index.html')
        asn2_d = asn2_r.json()
        asn2_data = asn2_d['data']

        # Build URL string for Your AS to get your current list of IXPs
        asn1_l = asn1_d['data'][0]['netixlan_set']
        asn1_ix = []
        for i in asn1_l:
            asn1_ix.append(i['ix_id'])
        asn1_ixs = str(asn1_ix).strip('[]',)
        asn1_ixs = ''.join([x for x in asn1_ixs.split(' ')])

        # Request Peer AS information based on only Your AS IXPs
        ixp_info = 'https://www.peeringdb.com/api/netixlan?asn=%s&ix_id__in=%s' % (asn2, asn1_ixs)
        ixp_info = requests.get(ixp_info)
        ixp_info = ixp_info.json()
        ixp_data = ixp_info['data']

        # Return the information
        return render_template('output.html', asn2_data=asn2_data, ixp_data=ixp_data)

if __name__ == '__main__':
    app.run()
