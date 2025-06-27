from flask import Flask, render_template, request, redirect, session, url_for, send_file
import pdfkit

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session

@app.route('/')
def home():
    return redirect(url_for('step1'))

@app.route('/step1', methods=['GET', 'POST'])
def step1():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']

        if len(name) < 3 or len(name) > 50:
            error = "Name must be between 3 and 50 characters."
        elif not mobile.isdigit() or len(mobile) != 10:
            error = "Mobile number must be exactly 10 digits."
        else:
            session['name'] = name
            session['email'] = email
            session['mobile'] = mobile
            return redirect(url_for('step2'))

    return render_template('step1.html', error=error)

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        session['address'] = request.form['address']
        session['city'] = request.form['city']
        session['state'] = request.form['state']
        session['country'] = request.form['country']
        return redirect(url_for('step3'))
    return render_template('step2.html')

@app.route('/step3', methods=['GET', 'POST'])
def step3():
    if request.method == 'POST':
        session['education'] = request.form['education']
        return redirect(url_for('step4'))
    return render_template('step3.html')

@app.route('/step4', methods=['GET', 'POST'])
def step4():
    if request.method == 'POST':
        session['experience'] = request.form['experience']
        return redirect(url_for('step5'))
    return render_template('step4.html')

@app.route('/step5', methods=['GET', 'POST'])
def step5():
    if request.method == 'POST':
        session['certifications'] = request.form['certifications']
        return redirect(url_for('preview'))
    return render_template('step5.html')

@app.route('/preview')
def preview():
    return render_template('preview.html', data=session)

@app.route('/download')
def download():
    rendered = render_template('resume_pdf.html', data=session)
    pdfkit.from_string(rendered, 'resume.pdf')
    return send_file('resume.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

    
