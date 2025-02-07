from supabase_py import create_client

# Initialize Supabase client
supabase_url = 'https://lhcpvlzksihcncnuoelx.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxoY3B2bHprc2loY25jbnVvZWx4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMyODE3MzcsImV4cCI6MjAyODg1NzczN30.SaD2nniti_XV-a24G7YWQy2dK37Rx4bJZ6TJga8Tj4U'
supabase = create_client(supabase_url, supabase_key)



